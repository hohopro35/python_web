import telebot
from telebot import types
import datetime
import googletrans
from googletrans import Translator
translator = Translator()

import codecs
bot = telebot.TeleBot("5279352357:AAHh7virskpdEEXgsP69XlS-BpoNYjjvcaM")

@bot.message_handler(commands=["start"])
def start(message):
    delete = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Приветствую!', reply_markup=delete)
    bot.send_message(message.chat.id, 'Я бот Stupenik.', reply_markup=delete)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('НАЧАТЬ')
    markup.add(button_start)
    bot.send_message(message.chat.id, 'Буду напоминать тебе, о домашнем задании  : )', reply_markup=markup)
    bot.register_next_step_handler(message, get_start)

@bot.message_handler(text=['НАЧАТЬ'])
def get_start(message):
    types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hw_for_yesterday = types.KeyboardButton("Задания на завтра")
    button_add = types.KeyboardButton('добавить Д/З')
    markup.add(button_hw_for_yesterday)

    markup.add(button_add)
    bot.send_message(message.chat.id, 'Выбери действие: ', reply_markup=markup)
    bot.register_next_step_handler(message, choose)

@bot.message_handler(content_types=['text'])
def choose(message):
    if message.text == 'Задания на завтра':
        hw_yesterday(message)
    if message.chat.id == 813629853 or message.chat.id == 950130682:
        if message.text == 'добавить Д/З':
            bot.send_message(message.chat.id, 'Введите формулу д/з:')
            bot.register_next_step_handler(message, add_homework)

@bot.message_handler(content_types=['text'])
def hw_yesterday(message):
    basa_homework = 'basa/homework/yesterday.txt'
    read_basa_hw = codecs.open(basa_homework, "r", 'utf8').read()
    data = read_basa_hw.split('/')
    date = int(datetime.datetime.now().date().day)
    date2 = int(datetime.datetime.now().date().month)
    n = len(data)
    for i in range(0, n):
        data_f = data[i].split('*')
        print(data_f)

        data_hw = data_f[0]
        data_hw2 = data_f[1].split('-')

        data_hw3 = data_hw2[0]
        data_hw3 = int(data_hw3)
        data_f = int(data_hw2[1])

        data_write = str(data_f)
        write_hw = str(data_hw)
        if data_hw3 >= date2:
            if data_hw3 > date2 and data_f < 2:
                bot.send_message(message.chat.id, write_hw)
            elif data_hw3 <= date2:
                if data_f >= date and data_f <= date + 1:
                    bot.send_message(message.chat.id, write_hw)

@bot.message_handler(content_types=['text'])
def add_homework(message):
    if message.chat.id == 813629853 or message.chat.id == 950130682:
        basa_homework = 'basa/homework/yesterday.txt'
        message = str(message.text)
        read_basa_hw_r = codecs.open(basa_homework, "r", 'utf8').read()
        read_basa_hw = codecs.open(basa_homework, "w", 'utf8')
        read_basa_hw.write('%s %s %s' % (read_basa_hw_r, '/', message))
        read_basa_hw.close()


bot.polling()
