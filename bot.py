from dotenv import load_dotenv
import os
import random
import telebot
from telebot import types

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))
    return image_files

@bot.message_handler(commands=['photo'])
def start_photo_game(message):
    photo_paths = get_image_files("./Images Data/")
    points = 0
    for i in range(5):
        random_photo_path = random.choice(photo_paths)
        send_photo(random_photo_path, message)
        answer = "AI" if "AI" in random_photo_path else "Human"
        points = handle_photo_callback(message, answer, points)

def handle_photo_callback(message, answer, points):
    inline_notification = types.InlineKeyboardMarkup()
    inline_notification.add(types.InlineKeyboardButton("AI", callback_data="AI"))
    inline_notification.add(types.InlineKeyboardButton("Human", callback_data="Human"))
    msg = bot.send_message(message.chat.id, "Is this AI or a human created image", reply_markup=inline_notification)
    return points

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    response = call.data
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if response == answer:
        points += 1
        bot.reply_to(call.message, f"Correct! Your points: {points}")
    else:
        bot.reply_to(call.message, "Incorrect! Try again.")

def send_photo(path, message):
    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    bot.reply_to(message, "Sending you a photo")

def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))
    return image_files

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()

