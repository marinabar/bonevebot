import json

import telebot
from telebot import types
import random

from telebot.types import InlineKeyboardMarkup
import re  # For preprocessing
import random
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency

# import spacy  # For preprocessing

import logging  # Setting up the loggings to monitor gensim

import gensim
from gensim import corpora, models, similarities
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors, Word2Vec

m = 'ruwikiruscorpora-superbigrams_skipgram_300_2_2018.vec.gz'

if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)


def str_generate():
    num_words = random.randint(2, 4)  # генерируем количество слов в пункте расписания
    first_word = random.randint(0, 746694)  # выбирает первое слово в расписании
    last_word_1 = list(model.wv.vocab.keys())[first_word]

    if type(last_word_1) != str:
        last_word = last_word_1[0]
    else:
        last_word = last_word_1

    ans = ""  # итоговый пункт расписания
    for i in range(num_words):
        if type(last_word) != str:
            last_word = last_word[0]
        last_word = str(last_word)

        list_of_words = last_word.split('_')
        ans += " ".join(list_of_words[0].split('::')) + ' '
        last_word = model.most_similar(negative=[last_word], topn=10)[random.randint(0, 9)]
    return ans


token = "933631111:AAHNKeuuKPbkc8a0i1fsrPwKLpQ0j2PUhjU"
# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

bot = telebot.TeleBot(token=token)

# get the first line if this is the one with the words words
text= open("word_rus.txt", "rb").read().decode("utf-8")
lines = text.split()
o=random.randint(1,len(lines))
line = lines[o]
raspi={'8:30': str_generate(), '9:00': str_generate(), '10:00': str_generate(), '11:30': str_generate(),
       '12:00': str_generate(), '14:00': str_generate(), '15:00': str_generate(), '16:30': str_generate(),
       '17:00': str_generate(), '18:30': str_generate(), '19:00': str_generate(), '20:00': str_generate(),
       '22:00': str_generate(), '00:00': str_generate()}


#raspi0=for key, val in raspi:
@bot.message_handler(commands=["start"])
def start(message):
    text = message.text
    user = message.chat.id
    print(user)
    markup = types.ReplyKeyboardMarkup()
    new = types.InlineKeyboardButton(text="generate raspi", callback_data='gener')
    markup.add(new)
    bot.send_message(user, text='→', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    user = message.chat.id
    if message.text == "generate raspi":
        markup1 = types.InlineKeyboardMarkup(row_width=2)
        for nom in raspi:
            button = types.InlineKeyboardButton(text= nom + ' ' + raspi[nom], callback_data=nom)
            markup1.add(button)
        bot.send_message(user, "choose", reply_markup=markup1)
        markup3 = types.ReplyKeyboardMarkup(row_width=2)
        ok = types.InlineKeyboardButton(text="Всё ок, давай в канал", callback_data="ok")
        again = types.InlineKeyboardButton(text="Сгенерировать заново", callback_data="generagain")
        markup3.add(ok,again)
        bot.send_message(user, text='ツ', reply_markup=markup3)


@bot.message_handler(content_types=['text'])
def text_again(message):
    if message.text=="Всё ок, давай в канал":
        texti= "".join(map(lambda x:"{}: {}".format(x[0], x[1]), raspi.items()))
        bot.send_message(boneve, text=texti)

@bot.message_handler(content_types=['text'])
def text_again(message):
    user = message.chat.id
    if message.text=="Сгенерировать заново":
        markup2 = types.InlineKeyboardMarkup(row_width=2)
        for bom in raspi:
            button1 = types.InlineKeyboardButton(text=bom + ' ' + raspi[bom], callback_data=bom)
            markup2.add(button1)
        bot.send_message(user, "choose", reply_markup=markup2)


# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline1(call):
    user = call.message.chat.id
    if call.message:
        for nom in raspi:
            if call.data == nom:
                markup4 = types.ReplyKeyboardMarkup()
                change = types.InlineKeyboardButton(text="Поменять", callback_data="change")
                markup4.add(change)
        bot.send_message(user, "choose", reply_markup=markup4)



bot.polling(none_stop=True)