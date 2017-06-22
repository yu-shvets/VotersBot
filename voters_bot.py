import telebot
from voters_address import districts, get_building_list, show_address
from telebot import types

token = '440200107:AAERzGyb7Od2WU7jNUZZKOnZeYRVk7DDNeg'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    for i in districts:
        button = types.KeyboardButton(i)
        markup.add(button)
    bot.reply_to(message, 'Привіт! Дізнайся адресу своєї виборчої дільниці у місті Києві. '
                          'Обери свій район:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in districts)
def district_input(message):
    file = open("district.txt", "w")
    file.write(message.text)
    file.close()
    bot.reply_to(message, 'Введи повну назву вулиці')


@bot.message_handler(func=lambda message: message.text[0].isdigit())
def address_output(message):
    file_1 = open("street.txt", "r")
    street_number = file_1.read()
    file_1.close()
    address = show_address(street_number, message.text)
    bot.send_message(message.chat.id, address)


@bot.message_handler(content_types=['text'])
def buildings_output(message):
    file = open("district.txt", "r")
    district = file.read()
    file.close()
    if get_building_list(district, message.text):
        street_number, buildings_list = get_building_list(district, message.text)
        file_1 = open("street.txt", "w")
        file_1.write(street_number)
        file_1.close()
        markup = types.ReplyKeyboardMarkup()
        for i in buildings_list:
            button = types.KeyboardButton(i)
            markup.add(button)
        bot.reply_to(message, 'Обери номер будинка:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Помилкові дані')


if __name__ == '__main__':
    bot.polling(none_stop=True)