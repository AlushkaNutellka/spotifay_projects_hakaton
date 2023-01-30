import requests
from bs4 import BeautifulSoup as b
import random
import telebot
URL = 'https://muzofond.fm/collections/artists/artik'
API_KEY = '5944770346:AAGmS8wOxJmkDvr0UIMaJQvCsjBn1gZmjQM'
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    a = soup.find_all('span', class_='track')
    # clear_bot = [c.span for c in a]
    random.shuffle(a)
    return a
    # return clear_bot


list_of_musik22 = parser(URL)
random.shuffle(list_of_musik22)

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['start'])

def hello(message):
    bot.send_message(message.chat.id, 'Хелоу Мэн! хочешь узнать лучшии песни за 10 лет, введи любую цифру ')


@bot.message_handler(content_types=['text'])
def pars(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_musik22[0])
        del list_of_musik22[0]
    else:
        bot.send_message(message.chat.id,'ЭЭ, Я ЖЕ СКАЗАЛ ЦИФР ДУБИНА!!!')


bot.polling()