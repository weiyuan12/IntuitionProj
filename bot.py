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
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    get_question(message.chat.id)

# Function to get a random question and send it to the user
def get_question(chat_id):
    question_data = random.choice(data)
    question = question_data['Input']
    answer = question_data['Answer']
    markup = generate_markup()
    bot.send_message(chat_id, question, reply_markup=markup)

# Function to create inline keyboard with two buttons
def generate_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("True", callback_data="True")
    button2 = types.InlineKeyboardButton("False", callback_data="False")
    markup.add(button1, button2)
    return markup

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "True" or call.data == "False":
        bot.answer_callback_query(call.id)
        # Get the correct answer for the current question
        correct_answer = next(item['Answer'] for item in data if item['Input'] == call.message.text)
        # Check if the user's choice matches the correct answer
        if call.data == correct_answer:
            response = "Correct! Well done!"
        else:
            response = "Wrong answer. Try again!"
        bot.send_message(call.message.chat.id, response)
        # Get the next question
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


bot.infinity_polling()