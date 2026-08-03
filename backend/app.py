import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware
from backend.prompts import SYSTEM_PROMPT
from backend.rag import search

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI(title="Liwin AI")
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
    question: str



@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/chat")
def chat(request: ChatRequest):

    try:
        # Retrieve relevant documents
        documents = search(request.question)

        context = "\n\n".join(documents)

        prompt = f"""
{SYSTEM_PROMPT}

=========================
KNOWLEDGE BASE
=========================

{context}

=========================
QUESTION
=========================

{request.question}

Instructions:

- Answer ONLY using the knowledge base.
- Speak in first person.
- If the answer is not found, reply:
"I don't have that information in my knowledge base."
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )


        return {
            "answer": response.text,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )