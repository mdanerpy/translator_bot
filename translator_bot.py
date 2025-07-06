from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
import os

def detect_language(text):
    # بررسی وجود حروف فارسی
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

if __name__ == '__main__':
    TOKEN = os.environ["BOT_TOKEN"]  # توکن رو از تنظیمات Render می‌گیره
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    print("ربات مترجم آماده اجراست...")
    app.run_polling()
