---
title: OrbitThink Chatbot
emoji: 🤖
colorFrom: purple
colorTo: indigo
sdk: docker
pinned: false
---
# OrbitThink Chatbot

A professional AI Chatbot for [OrbitThink Services](https://www.orbitthinkservices.com/), powered by RAG (Retrieval-Augmented Generation) technology.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![ChromaDB](https://img.shields.io/badge/Database-ChromaDB-orange)

## 🚀 Features

- **Custom Knowledge Base**: Ingests content from the OrbitThink website to answer user queries accurately.
- **RAG Architecture**: Uses ChromaDB for vector storage and Groq (Llama 3) for high-speed inference.
- **Professional Persona**: Tuned system prompts ensure the AI responds as a helpful, concise, and professional representative.
- **Embeddable Widget**: A clean, modern chat widget that can be easily added to any website.
- **Automated Scheduling**: Periodically scrapes the website to keep the knowledge base up-to-date.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/ML**: LangChain (logic), ChromaDB (Vector Store), Groq API (LLM)
- **Frontend**: Vanilla JavaScript, HTML/CSS (Widget)
- **Deployment**: Docker-ready, compatible with Render, Railway, Hugging Face Spaces.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/orbitthink007-creator/Chat_bot.git
    cd Chat_bot
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the `backend/` directory:
    ```ini
    GROQ_API_KEY=your_groq_api_key_here
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Run the application:**
    ```bash
    bash run.sh
    ```
    The backend will start at `http://localhost:8000`.

## 🌐 Deployment

This project is tailored for deployment on platforms like Render, Railway, or Hugging Face.

### Hugging Face Spaces (Recommended for Free Tier)
1.  Create a new Space (Docker SDK).
2.  Connect this repository.
3.  Add `GROQ_API_KEY` to the Space secrets.

### Render
1.  Create a Web Service connected to this repo.
2.  Use the build command: `pip install -r backend/requirements.txt`
3.  Use the start command: `gunicorn -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:10000`