from dotenv import load_dotenv
import os
import random

import telebot
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


@bot.message_handler(commands=['image'])
def send_images(message):
    global points 
    points = 0
    send_images_logic(message.chat.id)

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global points
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
    chat_id = call.message.chat.id
    send_images_logic(chat_id)
    



@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()