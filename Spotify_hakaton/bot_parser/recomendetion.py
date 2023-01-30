import requests
from bs4 import BeautifulSoup as b
import random
import telebot
API_KEY = '5944770346:AAGmS8wOxJmkDvr0UIMaJQvCsjBn1gZmjQM'
bot = telebot.TeleBot(API_KEY)
URL_ = 'https://wwv.zvuch.com/'


def pasers(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    a = soup.find_all('span', class_='track')
    random.shuffle(a)
    return a


rekc = pasers(URL_)
random.shuffle(rekc)


@bot.message_handler(commands=['recom'])
def rekom(message):
    bot.send_message(message.chat.id, 'Bro!!! посмотри реки,введи любую цифру от 1 до 9:)')


@bot.message_handler(content_types=['text'])
def pars(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, rekc[0])
        del rekc[0]
    else:
        bot.send_message(message.chat.id, 'БрОУЭ! ЦИФРЫ! АЛО!!!! АЛО!!!!')


bot.polling()
