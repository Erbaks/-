import telebot
import random

TOKEN = '7720116744:AAFPtlM4YsT02VAx3ALwOtkoQjfewmb_qRU'  # ← сюда вставь свой токен
bot = telebot.TeleBot(TOKEN)

# Храним данные игроков: загаданное число и оставшиеся попытки
user_data = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    number = random.randint(1, 100)
    user_data[message.chat.id] = {'number': number, 'attempts': 3}
    bot.send_message(message.chat.id, "Я загадал число от 1 до 100. У тебя 3 попытки, чтобы угадать!")

@bot.message_handler(func=lambda message: True)
def guess_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Нажми /start, чтобы начать новую игру.")
        return

    try:
        guess = int(message.text)
        game = user_data[chat_id]
        target = game['number']
        attempts = game['attempts']

        if guess == target:
            bot.send_message(chat_id, f"🎉 Поздравляю! Ты угадал число {target}!")
            del user_data[chat_id]
        else:
            game['attempts'] -= 1
            if game['attempts'] == 0:
                bot.send_message(chat_id, f"❌ Увы, ты проиграл. Загаданное число было {target}. Напиши /start, чтобы попробовать снова.")
                del user_data[chat_id]
            else:
                hint = "Меньше!" if guess > target else "Больше!"
                bot.send_message(chat_id, f"{hint} Осталось попыток: {game['attempts']}")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введи целое число от 1 до 100.")

bot.polling()
