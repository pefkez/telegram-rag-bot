import logging
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.config import settings
from app.rag_engine import index_document, ask_question, UPLOAD_DIR

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! Send me a PDF file, then ask questions about it."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    file = await update.message.document.get_file()
    file_path = UPLOAD_DIR / f"{user_id}_{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    try:
        num_docs = index_document(user_id, str(file_path))
        await update.message.reply_text(
            f"Document indexed ({num_docs} pages). Ask me anything about it!"
        )
    except Exception as e:
        await update.message.reply_text(f"Failed to index document: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    question = update.message.text

    answer, sources = ask_question(user_id, question)
    reply = answer
    if sources:
        reply += f"\n\nSources: {', '.join(set(sources))}"
    await update.message.reply_text(reply)
