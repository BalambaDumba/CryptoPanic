# bot.py

import requests
import time
import telebot
from config import *

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
posted_titles = set()

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
    news_items = get_crypto_news()
    for item in news_items:
        title = item['title']
        url = item['url']
        if title not in posted_titles:
            posted_titles.add(title)
            message = f"📰 <b>{title}</b>\n{url}"
            bot.send_message(CHAT_ID, message, parse_mode='HTML')

# Отправь /start боту, чтобы получить chat_id
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"Привет! Твой chat_id: {message.chat.id}")

if __name__ == "__main__":
    print("Бот запущен. Отправь /start своему боту в Telegram.")
    bot.polling(non_stop=True)

    while True:
        send_news()
        time.sleep(CHECK_INTERVAL)
