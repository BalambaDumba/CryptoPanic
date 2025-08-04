# bot.py

import requests
import time
import telebot
import os
from config import *

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
posted_titles = set()

# Загружаем chat_id, если он уже был сохранён
def load_chat_id():
    if os.path.exists("chat_id.txt"):
        with open("chat_id.txt", "r") as file:
            return file.read().strip()
    return None

# Сохраняем chat_id
def save_chat_id(chat_id):
    with open("chat_id.txt", "w") as file:
        file.write(str(chat_id))

CHAT_ID = load_chat_id()

def get_crypto_news():
    url = f'https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_API_KEY}&public=true'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print("Ошибка при получении новостей:", e)
        return []

def send_news():
    if not CHAT_ID:
        print("chat_id ещё не получен. Напиши боту команду /start.")
        return

    news_items = get_crypto_news()
    for item in news_items:
        title = item['title']
        url = item['url']
        if title not in posted_titles:
            posted_titles.add(title)
            message = f"📰 <b>{title}</b>\n{url}"
            bot.send_message(CHAT_ID, message, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    save_chat_id(CHAT_ID)
    bot.reply_to(message, f"Теперь бот будет присылать тебе новости!")

# Запускаем бота
if __name__ == "__main__":
    print("Бот запущен. Напиши /start боту в Telegram, чтобы он начал отправлять новости.")
    bot.polling(non_stop=True)

    while True:
        send_news()
        time.sleep(CHECK_INTERVAL)
