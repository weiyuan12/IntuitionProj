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

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    bot.reply_to(message, "Please use /start or /hello command to begin the interaction.")

# getting the input for random question?
@bot.message_handler(commands=['start'])
def choose_random_question_with_options(csv_file, bot, chat_id):
    # Read data from CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)

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

    return markup

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data in ("Correct", "Wrong"):
        bot.answer_callback_query(call.id)
        
        # Get the randomly chosen question
        random_question = get_random_question()
        
        # Find the correct answer for the randomly chosen question
        correct_answer = None
        for item in data:
            if item['wiki_intro'] == random_question:
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
        choose_random_question_with_options(csv_file, bot, call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, text="Invalid option selected")


# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     if call.data in ("Correct", "Wrong"):
#         bot.answer_callback_query(call.id)
#         # Get the correct answer for the current question
#         correct_answer = next(item['Correct/ Wrong'] for item in data if item['wiki_intro'] == call.message.text)
#         # Check if the user's choice matches the correct answer
#         if call.data == correct_answer:
#             response = "Congratulations! You are correct! 🎉"
#             # bot.send_sticker(call.message.chat.id, "STICKER_ID_OF_CELEBRATION_STICKER")
#         else:
#             response = "Oops! That's not correct. Better luck next time! 😕"
#         bot.send_message(call.message.chat.id, response)
#         # Get the next question
#         get_question(call.message.chat.id)
#     else:
#         bot.answer_callback_query(call.id, text="Invalid option selected")


# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#     get_question(message.chat.id)


def main():
    bot.polling(60)

if __name__ == '__main__':
    main()