import os
import random

import telebot
from telebot import types
import csv
import random
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Function to create inline keyboard with two buttons
def generate_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("1st", callback_data="first")
    button2 = telebot.types.InlineKeyboardButton("2nd", callback_data="second")
    markup.add(button1, button2)
    return markup

def generate_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("AI", callback_data="Correct")
    button2 = telebot.types.InlineKeyboardButton("Human", callback_data="Wrong")
    markup.add(button1, button2)
    return markup

def generate_markup_end(type):
    markup = telebot.types.InlineKeyboardMarkup()
    button3 = telebot.types.InlineKeyboardButton("End", callback_data="end")
    button4 = telebot.types.InlineKeyboardButton("Continue", callback_data=("continue" if type == "image" else "continueQ"))
    markup.add(button3, button4)
    return markup

# Function to choose a random image and return its path
def random_image(folder_path):
    # List all files in the folder
    image_files = os.listdir(folder_path)

    # Randomly select an image
    if image_files:
        selected_image = random.choice(image_files)
        image_path = os.path.join(folder_path, selected_image)
        return image_path
    else:
        print("No image files found in the folder.")

# Function to display 2 images and the 2 buttons
def send_images_logic(chat_id):
    global image_order
    image_order = random.randint(1,2) 
    bot.send_message(chat_id, 'Guess which one is AI generated!')
    if image_order == 1:
        with open(random_image("./Images Data/AI Generated"), 'rb') as photo:
            bot.send_photo(chat_id, photo)
        with open(random_image("./Images Data/Human Generated"), 'rb') as photo:
            bot.send_photo(chat_id, photo)
    elif image_order == 2:
        with open(random_image("./Images Data/Human Generated"), 'rb') as photo:
            bot.send_photo(chat_id, photo)
        with open(random_image("./Images Data/AI Generated"), 'rb') as photo:
            bot.send_photo(chat_id, photo)
        
    bot.send_message(chat_id, "Choose an option:", reply_markup=generate_markup())

# Function to run when the user types "/image"
@bot.message_handler(commands=['image'])
def send_images(message):
    global points, count
    points = 0
    count = 0
    send_images_logic(message.chat.id)


@bot.message_handler(commands=['question'])
def start(message):
    global points, count, answer
    points = 0
    count = 0
    answer = " "
    choose_random_question_with_options(message.chat.id)
# Function listens to the button click and tells user if right or wrong
# It also keeps track of points and repeats the game 
@bot.callback_query_handler(func=lambda call:call.data in ["first", "second"])
def query_handler(call):
    global points, count
    count +=1
    if image_order == 1:
        if call.data == "first":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Choosen: 1st. Correct! Yayyy!")
            points += 1
        elif call.data == "second":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Choosen: 2nd. Wrong, Nayyy...")
    elif image_order == 2:
        if call.data == "first":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Choosen: 1st. Wrong, Nayyy...")
        elif call.data == "second":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Choosen: 2nd. Correct! Yayyy!")
            points += 1
    
    bot.send_message(call.message.chat.id, f"Current points: {points}")
    bot.send_message(call.message.chat.id, "Continue?",  reply_markup=generate_markup_end("image"))
    


@bot.callback_query_handler(func=lambda call: call.data in ["continue", "end", "continueQ"])
def continue_or_end_handler(call):

    print("calling end handler")
    global points, count
    if call.data == "continue":
        chat_id = call.message.chat.id
        send_images_logic(chat_id)
    if call.data == "continueQ":
        chat_id = call.message.chat.id
        choose_random_question_with_options(chat_id)
    else:
        bot.send_message(call.message.chat.id, f"Game ended! Your final score: {points}/{count}")
            # Optionally, reset points and count for a new game
        points = 0
        count = 0


# Load data from CSV into a list of dictionaries
with open('wiki_genintro.csv', 'r', errors='ignore') as file:
    reader = csv.DictReader(file)
    question_data = list(reader)

# Function to choose a random question and send it to the user with options
def choose_random_question_with_options(chat_id):
    # Get the value from the "wiki_intro" column
    global answer
    random_row = random.choice(question_data)
    question = random_row['wiki_intro']
    answer = random_row["Correct/ Wrong"]  # Get the custom data
    # Encode the custom data in a hidden HTML input field
    bot.send_message(chat_id, f"{question}\n\nIs this AI generated or human written?", reply_markup=generate_markup() )

# Callback query handler
@bot.callback_query_handler(func=lambda call: call.data in ["Correct", "Wrong"] )
def query_handler(call):
    print("calling query handler")
    global points, count, answer
    count +=1
    print(call.message.entities)
    

    bot.answer_callback_query(call.id)
    print("User's choice:", call.data)
    print("Correct answer:", answer)

        # Check if the user's choice matches the correct answer
    if call.data == answer:
        response = "Congratulations! You are correct! 🎉"
        points +=1
    else:
        response = "Oops! That's not correct. Better luck next time! 😕"
        
        # Send the response to the user
    bot.send_message(call.message.chat.id, response)
        # Get the next question
    bot.send_message(call.message.chat.id, f"Current points: {points}")
    bot.send_message(call.message.chat.id, "Continue?",  reply_markup=generate_markup_end("question"))


# Infinite polling
bot.infinity_polling()
