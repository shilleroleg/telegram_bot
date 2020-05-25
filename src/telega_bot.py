import telebot as tb
from telebot import apihelper
import os
from flask import Flask, request
from random import choice
import config
import getweather as getw
import currencies
import stickerlist
import sql_database as sd

HEROKU = True

# Создаем бота

# Запускаем через прокси, если заблокировано
# # List proxy http://spys.one/proxys/US/  or  http://spys.one/socks/
# # apihelper.proxy = {'https': 'socks5://35.198.246.77:808'}
# # apihelper.proxy = {'https': 'socks5://181.102.135.183:1080'}
# apihelper.proxy = {'https': 'socks5://47.241.16.16:1080'}

bot = tb.TeleBot(config.TOKEN_TELEGRAM)

# Create sql database, for storage FLAG for weather in other town
con = sd.sql_connection()
sd.sql_create_table(con)

# Если послать боту комманду /start то отправит сообщение
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    if message.text == "/start":
        # Initial insert data in base
        entities = (message.from_user.id, 0)
        sd.sql_insert(con, entities)
        # ... and send message
        bot.send_message(message.chat.id, "Офигенски, погнали!")
    elif message.text == "/help":
        help_mess = """
Доступные комманды:
стикер - посылает случайный стикер.
погода - погода на данный момент.
прогноз - прогноз погоды на ближайшие 5 дней.
курс - курс валют"""
        bot.send_message(message.chat.id, help_mess)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "привет":           # Отвечает на сообщение
        bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name)

    elif message.text.lower() == "стикер":          # Отправляет стикер в ответ  на сообщение
        bot.send_sticker(message.chat.id, choice(stickerlist.sticker_list))

    elif message.text.lower() == "погода":
        keyboard = tb.types.InlineKeyboardMarkup(row_width=2)
        item1 = tb.types.InlineKeyboardButton("Новосибирск", callback_data='Nsk')
        item2 = tb.types.InlineKeyboardButton("Другой город", callback_data='Other')
        keyboard.add(item1, item2)

        bot.send_message(message.chat.id, "Где смотрим погоду?", reply_markup=keyboard)

    elif message.text.lower() == "прогноз":
        rt_lst = getw.forecast_weather_sparse_list()
        bot.send_message(message.chat.id, rt_lst[0])
        bot.send_message(message.chat.id, rt_lst[1])
        bot.send_message(message.chat.id, rt_lst[2])
        bot.send_message(message.chat.id, rt_lst[3])
        bot.send_message(message.chat.id, rt_lst[4])
    elif message.text.lower() == "курс":
        curr = currencies.get_currencies_pair()
        ans1 = "Курс валют на: {0}\nДоллар: {1}\nЕвро: {2}\nЮань: {3}\n".format(str(curr['time']), str(curr['usd']),
                                                                                str(curr['eur']), str(curr['cny']))
        ans2 = "Фунт: {0}\nГривна: {1}\nБел.руб.: {2}\nБиткоин: {3}$".format(str(curr['gbp']), str(curr['uah']),
                                                                             str(curr['byn']), str(curr['btc']))
        bot.send_message(message.chat.id, ans1 + ans2)

    elif sd.sql_select_flag(con, message.from_user.id) == 1:  # Проверяем погоду в другом городе по flag из sql базы
        # Set flag to 0
        sd.sql_update(con, 0, message.from_user.id)
        # Get weather
        bot.send_message(message.chat.id, get_weather(message.text))

    else:                                          # Повторяет сообщение в ответ
        bot.send_message(message.chat.id, "Ты сказал - " + message.text + "?")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Nsk':
                answer = get_weather('Novosibirsk')
                bot.send_message(call.message.chat.id, answer)
            elif call.data == 'Other':
                # Set flag to 1
                #
                sd.sql_update(con, 1, call.message.chat.id)

                bot.send_message(call.message.chat.id, 'В каком городе смотрим погоду?')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Погода", reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!")

    except Exception as e:
        print(repr(e))


# Бот при получении стикера печатает id стикера
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    print(message.sticker.file_id)


def get_weather(place='Novosibirsk'):
    weath_dict = getw.weather(place)
    str0 = place + " {0}\n".format(str(weath_dict['time']))

    str1 = "Температура: {0} C\nВлажность: {1}%\n".format(str(weath_dict['temperature']),
                                                          str(weath_dict['humidity']))
    str2 = "Давление {0} мм.рт.ст\nВетер: {1} м/с\n".format(str(int(weath_dict['pressure'] / 1.33322)),
                                                            str(weath_dict['wind']))
    str3 = "UV-индекс: {0}\nUV-риск: {1}\n".format(str(weath_dict['uv_val']),
                                                   str(weath_dict['uv_risk']))
    return str0 + str1 + str2 + str3


# Переменная HEROKU, чтобы наш бот отличал - запущен он на сервере или на локальной машине
if HEROKU:
    server = Flask(__name__)

    @server.route("/" + config.TOKEN_TELEGRAM, methods=['POST'])
    def getMessage():
        bot.process_new_updates([tb.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://young-hamlet-55059.herokuapp.com/" + config.TOKEN_TELEGRAM)
        return "!", 200
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=False)
else:
    # Если переменная HEROKU == False, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
