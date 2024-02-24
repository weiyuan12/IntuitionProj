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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    get_question(message.chat.id)

# Function to choose a random input 
def get_question(chat_id):
    question_data = random.choice(data)
    question = question_data['wiki_intro']
    markup = generate_markup()
    bot.send_message(chat_id, f"{question}\n\nIs this an AI generated intro, or one written by a human?", reply_markup=markup)

# Function to choose a random input 
def random_input(folder_path):
    # List all files in the folder
    input_files = os.listdir(folder_path)

    # Randomly select an image
    if input_files:
        selected_text = random.choice(input_files)
        input_path = os.path.join(folder_path, selected_text)
        return input_path
    else:
        print("No text files found in the folder.")


#######
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(call.id)
    correct_answer = None
    for item in data:
        if item['Question'] == call.message.text:
            correct_answer = item['Correct_Answer']
            break

    if call.data == correct_answer:
        response = "Correct! Well done!"
    else:
        response = f"Wrong answer. The correct answer is: {correct_answer}"
    bot.send_message(call.message.chat.id, response)

    # Ask the next question
    correct_answer = get_question(call.message.chat.id)

@bot.message_handler(commands=['start', 'quiz'])
def start_quiz(message):
    bot.reply_to(message, "Welcome to the quiz! Let's get started.")
    # Ask the first question
    get_question(message.chat.id)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    bot.reply_to(message, "Please use /start or /quiz command to begin the quiz.")

def main():
    bot.polling()

if __name__ == '__main__':
    main()



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


# def main():
#     bot.polling(60)

# if __name__ == '__main__':
#     main()
