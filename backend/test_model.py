import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-2.5-pro",
    "gemini-3.1-flash-lite"
]

for model in models:
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say Hello"
        )
        print(f"✅ {model}")
        print(response.text)
        break
    except Exception as e:
        print(f"❌ {model}")
        print(e)
        print("-" * 50)