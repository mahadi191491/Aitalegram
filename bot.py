import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import defaultdict, deque

from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters,
)

load_dotenv()
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant in a Telegram chat. Reply in the same "
    "language the user writes in. Keep answers short and clear.",
)

logging.basicConfig(level=logging.INFO)
client = genai.Client()  # reads GEMINI_API_KEY from env

# last 20 messages of memory per chat
history = defaultdict(lambda: deque(maxlen=20))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Amake kichu likho, ami reply dibo.")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history[update.effective_chat.id].clear()
    await update.message.reply_text("Memory clear kora hoyeche.")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    history[chat_id].append({"role": "user", "content": update.message.text})
    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    try:
        contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part(text=m["content"])],
            )
            for m in history[chat_id]
        ]
        resp = await client.aio.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        text = resp.text or "(khali reply ashlo)"
        history[chat_id].append({"role": "assistant", "content": text})
    except Exception:
        logging.exception("AI error")
        text = "Sorry, ekta error hoyeche. Pore abar try koro."
        history[chat_id].pop()
    await update.message.reply_text(text)


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"bot is running")

    def log_message(self, *args):
        pass


def start_health_server():
    # Render Web Service needs an open port
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), Health)
    threading.Thread(target=server.serve_forever, daemon=True).start()


def main():
    start_health_server()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()


if __name__ == "__main__":
    main()
