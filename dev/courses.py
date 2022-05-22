import requests
from globals import bot, valutes


def send_courses(message):
    req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    answer = ''
    for valute in valutes:
        answer += "{nom} {vlt} = {value} RUB\n".format(nom=req['Valute'][valute]['Nominal'], vlt=valute,
                                                       value=req['Valute'][valute]['Value'])
    bot.send_message(message.chat.id, answer)
