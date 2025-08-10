import os
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "").split(",")

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS stats (user_id INTEGER PRIMARY KEY, messages INTEGER)")
conn.commit()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот без валюты. Считаю твои сообщения 📊")

def stats(update: Update, context: CallbackContext):
    cursor.execute("SELECT messages FROM stats WHERE user_id=?", (update.effective_user.id,))
    row = cursor.fetchone()
    count = row[0] if row else 0
    update.message.reply_text(f"Ты отправил {count} сообщений.")

def log_message(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    cursor.execute("INSERT OR IGNORE INTO stats (user_id, messages) VALUES (?, ?)", (uid, 0))
    cursor.execute("UPDATE stats SET messages = messages + 1 WHERE user_id=?", (uid,))
    conn.commit()

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, log_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не задан в переменных окружения")
    else:
        main()
