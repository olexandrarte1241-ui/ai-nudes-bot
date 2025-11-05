import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, Update
from flask import Flask, request
import os

BOT_TOKEN = '8569739154:AAEb-QrW_ke4zILE9RX__OBlxvAFJEsbtDw'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Ціни в Stars
PRICES = [LabeledPrice(label='10 AI-нюдсів', amount=2500)]

WEBHOOK_URL = f"https://{os.environ.get('VERCEL_URL') or 'ai-nudes-bot.vercel.app'}"

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True))
        bot.process_new_updates([update])
        return 'OK', 200
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🔥 3 БЕЗКОШТОВНІ НЮДСИ", callback_data="free_nudes"))
    markup.add(InlineKeyboardButton("💎 КУПИТИ 10 НЮДСІВ (2500 Stars)", callback_data="buy_nudes"))
    bot.send_message(message.chat.id, "💋 Вітаю! Тестова версія:\nНатисни кнопку — отримай 3 гарячі AI-нюдси БЕЗКОШТОВНО!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "free_nudes":
        bot.send_message(call.message.chat.id, "🔥 Ось твої 3 тестові нюдси:")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_1.jpg")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_2.jpg")
        bot.send_photo(call.message.chat.id, "https://i.imgur.com/ai_test_3.jpg")

    elif call.data == "buy_nudes":
        bot.send_invoice(
            chat_id=call.message.chat.id,
            title='10 AI-нюдсів',
            description='Отримай 10 гарячих AI-нюдсів миттєво!',
            payload='10_nudes',
            provider_token='',
            currency='XTR',
            prices=PRICES
        )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def paid(message):
    bot.send_message(message.chat.id, "💎 Оплата пройшла! Ось 10 нюдсів:")
    for i in range(1, 11):
        bot.send_photo(message.chat.id, f"https://i.imgur.com/ai_paid_{i}.jpg")

# Авто-настройка webhook
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
