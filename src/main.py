from telebot import types
from globals import bot
from courses import send_courses
from patriotic_message import patriotic_message
from keyboards import menu_keyboard


@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Курс доллара")
    item2 = types.KeyboardButton("РОССИЯ!!!")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,
                     'Нажми: \n/course - для того чтоб узнать нынешний курс доллар\n /РОССИЯ!!! - вывести '
                     'патриотичное сообщение',
                     reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "РОССИЯ РОССИЯ РОССИЯ РОССИЯ РОССИЯ\n\n" +
                     "Для навигации используйте кнопки на клавиатуре\n\n",
                     reply_markup=menu_keyboard)


@bot.message_handler(content_types=["text"])
def menu(message):
    print(message.chat.id, message.text)

    command_list = {"курс валют к рублю": send_courses,
                    "россия!!!": patriotic_message
                    }

    if message.text.lower() in command_list.keys():
        command_list[message.text.lower()](message)
    else:
        bot.send_message(message.chat.id, "не понял", reply_markup=menu_keyboard)
        bot.register_next_step_handler(message, menu)

# Запускаем бота
bot.polling(none_stop=True, interval=0)
