import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import os

BOT_TOKEN = '8569739154:AAEb-QrW_ke4zILE9RX__OBlxvAFJEsbtDw'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 ОТРИМАТИ 3 БЕЗКОШТОВНІ НЮДСИ", callback_data="free_nudes"))
    bot.send_message(message.chat.id, "💋 Вітаю! Тестова версія:\nНатисни кнопку — отримай 3 гарячі AI-нюдси БЕЗКОШТОВНО!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "free_nudes":
        bot.send_message(call.message.chat.id, "🔥 Ось твої 3 тестові нюдси:")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_1.jpg")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_2.jpg")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_3.jpg")
        bot.send_message(call.message.chat.id, "👍 Круто? /start — ще раз!")

if __name__ == '__main__':
    bot.infinity_polling()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
