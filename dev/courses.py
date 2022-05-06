import requests
from globals import bot, valutes


def send_courses(message):
    req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    answer = ''
    for valute in valutes:
        answer += "1 {vlt} = {value} RUB\n".format(vlt=valute, value=req['Valute'][valute]['Value'])
    bot.send_message(message.chat.id, answer)