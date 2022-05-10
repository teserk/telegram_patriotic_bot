import schedule
from time import sleep
from threading import Thread
from telebot import types
from globals import bot
from courses import send_courses
from patriotic_message import patriotic_message
from keyboards import menu_keyboard
from mailing import do_mailing


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/course")
    item2 = types.KeyboardButton("РОССИЯ!!!")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,
                     'РОССИЯ!!! РОССИЯ!!! РОССИЯ!!! напиши /help для помощи\n',
                     reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "РОССИЯ РОССИЯ РОССИЯ РОССИЯ РОССИЯ\n\n" +
                     "Для навигации используйте кнопки на клавиатуре\n\n",
                     "Если вы подпишитесь на рассылку я каждый день в 8:21 МСК буду присылать изменение" +
                     " выбранной валюты в сравнении с предыдущим днём",
                     reply_markup=menu_keyboard)


@bot.message_handler(content_types=["text"])
def menu(message):
    print(message.chat.id, message.text)

    command_list = {"/course": send_courses,
                    "россия!!!": patriotic_message,
                    "/help": help
                    }

    if message.text.lower() in command_list.keys():
        command_list[message.text.lower()](message)
    else:
        bot.send_message(message.chat.id, "не понял", reply_markup=menu_keyboard)
        bot.register_next_step_handler(message, menu)

def time_checker():
    """
    Проверка времени
    """
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    # Рассылка
    schedule.every().day.at("05:21").do(do_mailing)
    Thread(target=time_checker).start()

    # Запуск бота
    bot.polling()