import telebot
from telebot import types
import os
import config

bot = telebot.TeleBot(config.token)

# Faylga foydalanuvchi ma'lumotlarini saqlash funksiyasi
DATA_FILE = 'user_data.txt'

def save_user_data(user_id, name, phone):
    with open(DATA_FILE, 'a') as f:  # 'a' rejimi ma'lumotlarni faylga qo'shib boradi
        f.write(f"Foydalanuvchi ID: {user_id}, Ismi: {name}, Telefon: {phone}\n")

# Telefon raqamini so'rash va kiritish
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = types.KeyboardButton(text="Telefon raqamni ulashish", request_contact=True)
    markup.add(phone_button)
    bot.send_message(chat_id, "Salom! Telefon raqamingizni quyidagi tugma orqali ulashing.", reply_markup=markup)

# Foydalanuvchi telefon raqamini yuborganda
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.chat.id
    if message.contact is not None:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        user_id = message.contact.user_id

        # Ma'lumotlarni faylga saqlash
        save_user_data(user_id, first_name, phone_number)

        # Asosiy menyuga o'tish
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Help")
        btn2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(btn1)#, btn2)
        bot.send_message(chat_id, text=f"Rahmat, {first_name} ! Ma'lumotlaringiz qabul qilindi.", reply_markup=markup)

@bot.message_handler(commands=['thelastman'])
def thelastman_command(message):
    bot.send_message(message.chat.id, text="Yordam kerakmi? Men bu yerda yordam bera olaman!")



@bot.message_handler(func=lambda message: message.text.startswith('@'))
def inline_bot_usage(message):
    bot.send_message(message.chat.id, "Siz inline bot orqali so'rov yubordingiz. Natija sizga taqdim etiladi.")



# Matnli xabarlarni qayta ishlash
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Help":
        bot.send_message(message.chat.id,"Bu bot nimalar qila oladi\n1. @ bilan ayrim kerakli narsalarni qidirishingiz mumkin. Masalan:\n├ @pic - rasmlarni qidirish (@pic mushuk)\n├ @gif - giflarni qidirish (@gif xursand)\n├ @vid - videolarni qidirish (@vid yomgirlar)\n├ @youtube - youtubedan narsa izlash qidirish (@youtube musiqa)\n├ @wiki - Wikipediadan malumot izlash (@wiki telegram) vhk")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif message.text == "Как меня зовут?":
        bot.send_message(message.chat.id, "У меня нет имени..")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")
    
    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Help")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

bot.polling(none_stop=True)
