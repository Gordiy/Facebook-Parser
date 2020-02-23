import time
import random
import telebot
import requests


token = '932417576:AAEH-AvLaWS9O0IOJ7hajkmgrrwRxqIwG8E'
bot = telebot.TeleBot(token)

user_id = None
group_url = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_id

    user_id = message.from_user.id
    user_murkup = telebot.types.ReplyKeyboardMarkup(True)
    user_murkup.row('Начать парсинг')

    bot.send_message(message.from_user.id, "Привет.", reply_markup=user_murkup)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Начать парсинг':
        msg = bot.send_message(message.from_user.id, "Введите ссылку на группу которую надо парсить")
        bot.register_next_step_handler(msg, start_parsing)

    else:
        user_murkup = telebot.types.ReplyKeyboardMarkup(True)
        user_murkup.row('/start')

        msg = bot.send_message(message.from_user.id, "Начните с начала.", reply_markup=user_murkup)
        bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(content_types=['text'])
def start_parsing(message):
    global group_url
    group_url = message.text

    group_url = group_url.replace('/', '_')

    resp = requests.get('http://127.0.0.1:8000/index/' + group_url)
    print(resp.text)
    if resp.status_code == 200:

        msg = bot.send_message(message.from_user.id, "Парсинг запущен. Введите сообщение для рассылки.")
        bot.register_next_step_handler(msg, send_message)
    else:
        bot.send_message(message.from_user.id, "Парсинг не запущен")
        user_murkup = telebot.types.ReplyKeyboardMarkup(True)
        user_murkup.row('/start')

        msg = bot.send_message(message.from_user.id, "Начните с начала.", reply_markup=user_murkup)
        bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(content_types=['text'])
def send_message(message):
    msg = message.text.replace(' ', '+')

    resp = requests.get('http://127.0.0.1:8000/send_msg/'+msg)
    if resp.status_code == 200:

        msg = bot.send_message(message.from_user.id, "Рассылка запущено. Ожидайте уведомления о сообщениях.")
        bot.register_next_step_handler(msg, read_count_message)
    else:
        bot.send_message(message.from_user.id, "Рассылка не запущена.")
        user_murkup = telebot.types.ReplyKeyboardMarkup(True)
        user_murkup.row('/start')

        msg = bot.send_message(message.from_user.id, "Начните с начала.", reply_markup=user_murkup)
        bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(content_types=['text'])
def read_count_message(message):

    while True:
        resp = requests.get('http://127.0.0.1:8000/count_msg')

        if resp.status_code == 200:
            response = resp.json()
            print(response)

            for data in response['count_messages']:

                text_for_user = 'Количество сообщений {0}, Логин: {1}, Пароль {2}'.format(data['count_msg'], data['login'], data['password'])
                bot.send_message(message.from_user.id, text_for_user)
        else:
            bot.send_message(message.from_user.id, "Возникли проблемы.")
            user_murkup = telebot.types.ReplyKeyboardMarkup(True)
            user_murkup.row('/start')

            msg = bot.send_message(message.from_user.id, "Начните с начала.", reply_markup=user_murkup)
            bot.register_next_step_handler(msg, send_welcome)

            break

        time.sleep(3600)



bot.skip_pending = True

while True:

    try:

        bot.polling(none_stop=True)

    except Exception as e:

        time.sleep(60)
