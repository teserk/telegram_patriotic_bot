import datetime
import requests

from globals import api_key, bot, valutes, users_database
from keyboards import mailing_keyboard, menu_keyboard, currency_keyboard


def mailing_for_main_menu(message):
    if users_database.user_is_subscribed(message.chat.id):
        user_currency = users_database.get_currency(message.chat.id)
        bot.send_message(message.chat.id, f"Сейчас вы подписаны и выбрана валюта валюта: {user_currency}",
                         reply_markup=mailing_keyboard)
    else:
        bot.send_message(message.chat.id, "Сейчас вы не подписаны", reply_markup=mailing_keyboard)
    bot.register_next_step_handler(message, mailing_menu)


def mailing_menu(message):
    """
    Основное меню рассылки
    """
    commands_list = {"подписаться": subscribe, "отписаться": unsubscribe, "выбрать валюту": set_currency_for_menu}
    if message.text.lower() in commands_list.keys():
        commands_list[message.text.lower()](message)
    elif message.text.lower() == "назад":
        bot.send_message(message.chat.id, "welcome to menu, buddy", reply_markup=menu_keyboard)
    else:
        bot.send_message(message.chat.id, "не понял", reply_markup=menu_keyboard)


def subscribe(message):
    """
    Подписывает пользователя на рассылку
    """
    if users_database.user_exists_in_database(message.chat.id):
        currency = users_database.get_currency(message.chat.id)
        if users_database.user_is_subscribed(message.chat.id):
            bot.send_message(message.chat.id,
                             f"Вы уже подписаны на рассылку, выбрананая валюта - {currency}",
                             reply_markup=mailing_keyboard)
        else:
            bot.send_message(message.chat.id,
                             f"Вы подписались на рассылку, выбрананая валюта - {currency}",
                             reply_markup=mailing_keyboard)
            users_database.update_user(message.chat.id, subscription=True)
    else:
        users_database.add_user(message.chat.id)
        bot.send_message(message.chat.id,
                         "Вы подписались на рассылку, установлена валюта по умолчанию - RUB",
                         reply_markup=mailing_keyboard)
    bot.register_next_step_handler(message, mailing_menu)


def unsubscribe(message):
    """
    Отписывает пользователя от рассылки
    """
    if users_database.user_exists_in_database(message.chat.id):
        users_database.update_user(message.chat.id, subscription=False)
    else:
        users_database.add_user(message.chat.id, subscription=False)
    bot.send_message(message.chat.id, "Вы отписались от рассылки")
    bot.register_next_step_handler(message, mailing_menu)


def set_currency_for_menu(message):
    bot.send_message(message.chat.id, "Выберите валюту (можно ввести свою)", reply_markup=currency_keyboard)
    bot.register_next_step_handler(message, set_currency)


def set_currency(message):
    """
    Записывает выбранную валюту в базу данных (для пользователя)
    """
    if message.text.upper() in valutes:
        if users_database.user_exists_in_database(message.chat.id):
            if users_database.user_is_subscribed(message.chat.id):
                bot.send_message(message.chat.id, f"Вы выбрали валюту {message.text.upper()}",
                                 reply_markup=mailing_keyboard)
            else:
                bot.send_message(message.chat.id, f"Вы выбрали валюту {message.text.upper()}, но все еще не подписаны",
                                 reply_markup=mailing_keyboard)
            users_database.update_user(message.chat.id, currency=message.text.upper())

        else:
            bot.send_message(message.chat.id,
                             f"Вы выбрали валюту {message.text.upper()} и были автоматически подписаны",
                             reply_markup=mailing_keyboard)
            users_database.add_user(message.chat.id, currency=message.text.upper())

        bot.register_next_step_handler(message, mailing_menu)
    else:
        bot.send_message(message.chat.id, "Я не знаю такую валюту", reply_markup=mailing_keyboard)
        bot.register_next_step_handler(message, mailing_menu)


def do_mailing():
    """
    Рассылает всем подписанным ползьователям изменение курса выбранной валюты в сравнении с предыдущим днем
    """
    today = datetime.date.today()
    today = str(today.strftime("%Y-%m-%d"))
    today_request = requests.get(f"http://data.fixer.io/api/{today}", params={"access_key": api_key}).json()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = str(yesterday.strftime("%Y-%m-%d"))
    yesterday_request = requests.get(f"http://data.fixer.io/api/{yesterday}", params={"access_key": api_key}).json()
    for user in users_database.subscribed_users():
        user_id = user[0]
        currency = user[1]
        today_cost = today_request["rates"][currency]
        today_cost_rub = round(today_request["rates"]["RUB"] / today_request["rates"][currency], 5)

        yesterday_cost = yesterday_request["rates"][currency]
        yesterday_cost_rub = round(today_request["rates"]["RUB"] / yesterday_request["rates"][currency], 5)

        difference = today_cost_rub - yesterday_cost_rub

        bot.send_message(user_id, "РАССЫЛКА")
        if difference > 0:
            bot.send_message(user_id,
                             f"Сегодня {currency} вырос с {yesterday_cost} ({yesterday_cost_rub} RUB) до " +
                             f"{today_cost} ({today_cost_rub} RUB) (на {round(difference, 8)} RUB)",
                             reply_markup=menu_keyboard)
        elif difference < 0:
            bot.send_message(user_id,
                             f"Сегодня {currency} упал с {yesterday_cost} ({yesterday_cost_rub} RUB) до " +
                             f"{today_cost} ({today_cost_rub} RUB) (на {round(difference, 8)} RUB)",
                             reply_markup=menu_keyboard)
        else:
            bot.send_message(user_id,
                             f"Сегодня {currency} не изменился",
                             reply_markup=menu_keyboard)