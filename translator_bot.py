from telegram.ext import Updater, MessageHandler, Filters
import requests

TOKEN = "7770288470:AAFXjj4hkZ3q7vsc8zt7AFHmbpLNA-GAY-4"

def detect_lang(text):
    persian_letters = set("اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
    count = sum(1 for ch in text if ch in persian_letters)
    return "fa" if count > len(text) / 3 else "en"

def translate(text, source, target):
    url = "https://libretranslate.de/translate"
    payload = {"q": text, "source": source, "target": target, "format": "text"}
    response = requests.post(url, json=payload)
    return response.json().get("translatedText", "خطا در ترجمه")

def handle_message(update, context):
    text = update.message.text
    lang = detect_lang(text)
    target = "en" if lang == "fa" else "fa"
    translated = translate(text, lang, target)
    update.message.reply_text(translated)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("ربات آماده‌ست...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()