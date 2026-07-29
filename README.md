# Telegram RAG Bot

Загружаешь PDF в Telegram бота — задаёшь вопросы, он отвечает по содержанию документа (RAG).

```
pip install -r requirements.txt
```

Скопировать `.env.example` → `.env`, вставить `TELEGRAM_TOKEN` (от @BotFather) и `OPENAI_API_KEY`.

```
python run.py
```

Кидаешь боту PDF, потом пишешь вопросы — он ищет ответы в документе.
