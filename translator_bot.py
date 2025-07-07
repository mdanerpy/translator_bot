from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def detect_language(text):
    for ch in text:
        if '\u0600' <= ch <= '\u06FF':
            return 'fa'
    return 'en'

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = detect_language(text)

    if lang == 'fa':
        translated = GoogleTranslator(source='auto', target='en').translate(text)
    else:
        translated = GoogleTranslator(source='auto', target='fa').translate(text)

    await update.message.reply_text(translated)

def fake_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("", port), BaseHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    # اجرای پورت الکی برای فریب Render
    threading.Thread(target=fake_server).start()

    # اجرای ربات
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    print("✅ ربات مترجم آماده اجراست...")
    app.run_polling()
