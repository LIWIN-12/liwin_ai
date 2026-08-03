from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("liwin")

# Clear existing data (optional during development)
try:
    collection.delete(ids=collection.get()["ids"])
except Exception:
    pass

knowledge_path = Path("knowledge")

documents = []
ids = []

for file in knowledge_path.glob("*.md"):
    print(f"Reading {file.name}")

    text = file.read_text(encoding="utf-8")

    documents.append(text)
    ids.append(file.stem)

print("Creating embeddings...")

embeddings = model.encode(documents).tolist()

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)

print(f"Indexed {len(documents)} documents successfully!")