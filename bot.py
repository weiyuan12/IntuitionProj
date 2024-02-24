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

# Function to choose a random question and send it to the user with options
def choose_random_question_with_options(bot, chat_id):
    # Choose a random row
    random_row = random.choice(data)

    # Get the value from the "wiki_intro" column
    question = random_row['wiki_intro']

    # Create inline keyboard markup with two option buttons
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("AI Generated", callback_data="Correct")
    button2 = types.InlineKeyboardButton("Human Written", callback_data="Wrong")
    markup.add(button1, button2)

    # Ask the user the question and provide option buttons
    bot.send_message(chat_id, f"{question}\n\nIs this AI generated or human written?", reply_markup=markup)

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data in ("Correct", "Wrong"):
        bot.answer_callback_query(call.id)
        
        # Find the correct answer for the randomly chosen question
        correct_answer = None
        for item in data:
            if item['wiki_intro'] == call.message.text:
                correct_answer = item['Correct/ Wrong']
                break

        # Check if the user's choice matches the correct answer
        if call.data == correct_answer:
            response = "Congratulations! You are correct! 🎉"
        else:
            response = "Oops! That's not correct. Better luck next time! 😕"
        
        # Send the response to the user
        bot.send_message(call.message.chat.id, response)

        # Get the next question
        choose_random_question_with_options(bot, call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, text="Invalid option selected")


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    choose_random_question_with_options(bot, message.chat.id)

# Infinite polling
def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
