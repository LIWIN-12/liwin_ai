# 🤖 Liwin AI

An AI-powered personal portfolio assistant built with **FastAPI**, **Google Gemini**, **ChromaDB**, and **Retrieval-Augmented Generation (RAG)**.

Liwin AI answers questions about my education, projects, skills, experience, certifications, achievements, and career using a custom knowledge base.

---

## 🚀 Features

- AI-powered portfolio assistant
- Retrieval-Augmented Generation (RAG)
- Google Gemini integration
- ChromaDB vector database
- Semantic search using Sentence Transformers
- FastAPI backend
- Responsive HTML, CSS, and JavaScript frontend
- Markdown-based knowledge base
- Easy to extend with new documents

---

## 🏗️ Project Structure

```
liwin-ai/
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   ├── prompts.py
│   ├── ingest.py
│   ├── requirements.txt
│   └── __init__.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── knowledge/
│   ├── about.md
│   ├── education.md
│   ├── experience.md
│   ├── projects.md
│   ├── skills.md
│   └── ...
│
├── chroma_db/
│
├── .env
└── README.md
```

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn

### AI

- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- all-MiniLM-L6-v2

### Database

- ChromaDB (Vector Database)

### Frontend

- HTML5
- CSS3
- JavaScript

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/liwin-ai.git

cd liwin-ai
```

---

### Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

### Build the vector database

```bash
python backend/ingest.py
```

---

### Run the application

```bash
uvicorn backend.app:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

## 💬 Example Questions

- Tell me about yourself
- What are your technical skills?
- Tell me about Smart Focus
- What projects have you built?
- What certifications do you have?
- What is your education?
- What technologies do you use?
- What are your career goals?

---

## 🧠 How It Works

```
User Question
      │
      ▼
FastAPI Backend
      │
      ▼
Generate Embedding
      │
      ▼
Search ChromaDB
      │
      ▼
Retrieve Relevant Knowledge
      │
      ▼
Build Prompt
      │
      ▼
Google Gemini
      │
      ▼
AI Response
```

---

## 📚 Knowledge Base

The assistant retrieves information from Markdown files located in the `knowledge/` directory.

Examples include:

- About
- Education
- Experience
- Skills
- Projects
- Achievements
- Certifications
- Career Goals
- Personality
- FAQs

---

## 🔮 Future Improvements

- Document chunking
- Conversation memory
- Streaming responses
- Voice interaction
- Multi-language support
- Local LLM support (Ollama)
- Docker deployment
- Admin dashboard
- Analytics

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

## 👤 Author

**J. K. Liwin Jose**

AI & Data Science Graduate

Software Analyst

Passionate about Artificial Intelligence, Machine Learning, Computer Vision, Backend Development, and Intelligent Software Systems.

---

## ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.