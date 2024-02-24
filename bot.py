import os
import telebot
from telebot import types
import csv
import random
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Load data from CSV into a list of dictionaries
with open('wiki_genintro.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    get_question(message.chat.id)

# Function to get a random question and send it to the user
def get_question(chat_id):
    question_data = random.choice(data)
    question = question_data['wiki_intro']
    answer = question_data['Correct/ Wrong']
    markup = generate_markup()
    bot.send_message(chat_id, f"{question}\n\nIs this an AI generated intro, or one written by a human?", reply_markup=markup)

# Function to create inline keyboard with two buttons
def generate_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("AI Generated", callback_data="True")
    button2 = types.InlineKeyboardButton("Human Written", callback_data="False")
    markup.add(button1, button2)
    return markup

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "True" or call.data == "False":
        bot.answer_callback_query(call.id)
        # Get the correct answer for the current question
        correct_answer = next(item['Correct/ Wrong'] for item in data if item['wiki_intro'] == call.message.text)
        # Check if the user's choice matches the correct answer
        if call.data == correct_answer:
            response = "Congratulations! You are correct! 🎉"
            # Send a sticker
            bot.send_sticker(call.message.chat.id, "STICKER_ID_OF_CELEBRATION_STICKER")
        else:
            response = "Oops! That's not correct. Better luck next time! 😕"
        bot.send_message(call.message.chat.id, response)
        # After sending the response, ask a new question
        get_question(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, text="Invalid option selected")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def main():
    bot.polling()

if __name__ == '__main__':
    main()


# bot.infinity_polling()