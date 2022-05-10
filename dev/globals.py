import telebot
from DB import UsersDB


API_TOKEN = '-----'
bot = telebot.TeleBot(API_TOKEN)
valutes = ['USD', 'EUR', 'GBP', 'KZT']
api_key = "----"
users_db = UsersDB()
