import logging

from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.config import settings
from app.bot import start, handle_document, handle_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telegram RAG Bot")

telegram_app = Application.builder().token(settings.telegram_token).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@app.on_event("startup")
async def on_startup():
    webhook_url = f"{settings.webhook_url.rstrip('/')}/webhook"
    await telegram_app.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to {webhook_url}")


@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.bot.delete_webhook()


@app.post("/webhook")
async def webhook(request: Request) -> None:
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)


@app.get("/health")
async def health():
    return {"status": "ok"}
