import time
import telebot
import requests
from Parser.login_config import telegram_token, login, pswd


bot = telebot.TeleBot(telegram_token)

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

        bot.send_message(message.from_user.id, "Парсинг запущен")
    else:
        bot.send_message(message.from_user.id, "Парсинг не запущен")


bot.skip_pending = True

while True:

    try:

        bot.polling(none_stop=True)

    # ConnectionError and ReadTimeout because of possible timout of the requests library

    # TypeError for moviepy errors

    # maybe there are others, therefore Exception

    except Exception as e:


        time.sleep(15)

