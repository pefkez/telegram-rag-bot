# Telegram RAG Bot

AI-powered Telegram bot that answers questions from uploaded PDF documents using RAG (Retrieval-Augmented Generation).

## Stack

- **FastAPI** — web server & Telegram webhook
- **LangChain** — LLM orchestration
- **LlamaIndex** — document indexing & retrieval
- **OpenAI** — embeddings & chat completions
- **python-telegram-bot** — Telegram integration

## Features

- Upload PDF files to a Telegram chat
- Ask questions about the uploaded documents
- AI answers based on retrieved content (RAG)
- Persistent document index per user

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in:
   - `TELEGRAM_TOKEN` — your bot token from @BotFather
   - `OPENAI_API_KEY` — your OpenAI API key
4. Run:
   ```bash
   python run.py
   ```

## Usage

1. Start a chat with your bot on Telegram
2. Send a PDF file
3. Ask questions about the document
4. The bot retrieves relevant chunks and answers via AI

## Project Structure

```
telegram-rag-bot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app & webhook
│   ├── bot.py           # Telegram bot handlers
│   ├── rag_engine.py    # RAG pipeline (LlamaIndex + LangChain)
│   ├── models.py        # Pydantic models
│   └── config.py        # Settings
├── requirements.txt
├── run.py
└── README.md
```
