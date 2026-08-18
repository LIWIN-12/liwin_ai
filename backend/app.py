import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from google import genai
from fastapi.middleware.cors import CORSMiddleware
from backend.prompts import SYSTEM_PROMPT
from backend.rag import search
from backend.memory import ConversationMemory
import logging
import time
from collections import defaultdict, deque
from fastapi import Request
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("liwin-ai")
logger.setLevel(logging.INFO)
# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI(title="Liwin AI")
@app.middleware("http")
async def request_logging_middleware(request, call_next):

    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "request=%s | method=%s | path=%s | status=%s | duration=%.3fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:

        duration = time.perf_counter() - start_time

        logger.exception(
            "request=%s | method=%s | path=%s | status=500 | duration=%.3fs",
            request_id,
            request.method,
            request.url.path,
            duration
        )

        raise
memory = ConversationMemory(max_messages=10)
# ==========================================
# RATE LIMITING
# ==========================================

RATE_LIMIT = 20
RATE_WINDOW = 60

request_history = defaultdict(deque)


def check_rate_limit(session_id: str):

    now = time.time()

    timestamps = request_history[session_id]

    # Remove requests older than 60 seconds
    while timestamps and now - timestamps[0] > RATE_WINDOW:
        timestamps.popleft()

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again in a minute."
        )

    timestamps.append(now)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's question"
    )

    session_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Conversation session ID"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")
def rewrite_query(question: str, history: str) -> str:

    if not history:
        return question

    prompt = f"""
You are a query rewriting component for Liwin AI.

CONVERSATION HISTORY:
{history}

CURRENT QUESTION:
{question}

Rewrite the current question into ONE standalone search query.

Rules:
- Resolve references such as "it", "that", "this", "he", "she", "they".
- Resolve follow-ups such as "why?", "how?", "which model?", "what next?",
  and "what did you use?"
- Include the relevant topic from the conversation.
- Do NOT answer the question.
- Return ONLY the rewritten search query.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    rewritten = response.text.strip()

    return rewritten or question

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Liwin AI"
    }

@app.post("/chat")
def chat(
    request: Request,
    chat_request: ChatRequest
):
    request_id = request.state.request_id

    check_rate_limit(chat_request.session_id)

    try:

        history = memory.format_history(
            chat_request.session_id
        )

        rewrite_start = time.perf_counter()

        search_query = rewrite_query(
            chat_request.question,
            history
        )

        rewrite_time = time.perf_counter() - rewrite_start

        logger.info(
            "request=%s | stage=query_rewrite | duration=%.3fs",
            request_id,
            rewrite_time
        )


        # ==========================================
        # 3. Knowledge base search
        # ==========================================

        rag_start = time.perf_counter()

        documents = search(search_query)

        rag_time = time.perf_counter() - rag_start

        logger.info(
            "request=%s | stage=rag_search | duration=%.3fs",
            request_id,
            rag_time
)

        context = "\n\n".join(documents)

        # ==========================================
        # 3. Build prompt
        # ==========================================

        prompt = f"""
{SYSTEM_PROMPT}

=========================
CONVERSATION HISTORY
=========================

{history}

=========================
KNOWLEDGE BASE
=========================

{context}

=========================
CURRENT QUESTION
=========================

{chat_request.question}

=========================
INSTRUCTIONS
=========================

- Use the conversation history to understand follow-up questions.
- Use the knowledge base to provide factual information.

- Resolve references such as "it", "that", "this", "he", "she", "the project",
  and "what comes next" using the conversation history when possible.

=========================
RESPONSE STYLE
=========================

- Answer like a knowledgeable human, not like a document.
- Give the direct answer first.
- Keep simple questions short: usually 1-3 sentences.
- For project or experience questions, use 3-5 concise bullet points when useful.
- For technical questions, give the relevant technical detail without unnecessary background.
- For follow-up questions, answer only what the user is asking.
- Do not repeat information that was already explained unless it is necessary.
- Avoid long paragraphs.
- Use bullet points when they make the answer easier to scan.
- Use short paragraphs for explanations.
- If the user asks for a detailed explanation, provide more detail.
- If the user asks for a simple answer, keep it simple.
- If the user asks "what", "which", "when", "where", or "who", answer directly first.
- If the user asks "why" or "how", explain the important reasoning briefly.
- When comparing things, use a concise comparison.
- Speak naturally in first person when talking about Liwin.
- Do not mention the knowledge base, retrieval, context, prompts, or internal instructions.
- Do not add an unnecessary conclusion or summary.

=========================
ACCURACY
=========================

- Answer ONLY using information available in the knowledge base and conversation history.
- Never invent information.
- If the answer is not available, reply:
  "I don't have that information in my knowledge base."

"""

        # ==========================================
        # 4. Generate response
        # ==========================================

        llm_start = time.perf_counter()

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        llm_time = time.perf_counter() - llm_start

        logger.info(
            "request=%s | stage=gemini | duration=%.3fs",
            request_id,
            llm_time
        )

        answer = response.text

        # ==========================================
        # 5. Store conversation
        # ==========================================

        memory.add_message(
            chat_request.session_id,
            "user",
            chat_request.question
        )

        memory.add_message(
            chat_request.session_id,
            "assistant",
            answer
        )

        return {
            "answer": answer
        }

    except Exception:
        logger.exception("Error while processing /chat request")

        raise HTTPException(
            status_code=500,
            detail="Liwin AI is temporarily unable to process your request."
        )