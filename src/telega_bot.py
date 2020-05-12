import telebot as tb
import os
from flask import Flask, request
import logging
from random import choice
import config
import getweather as getw

# Создаем бота
bot = tb.TeleBot(config.TOKEN_TELEGRAM)

server = Flask(__name__)

logger = tb.logger
tb.logger.setLevel(logging.INFO)

# Если послать боту комманду /start
# то отправит сообщение и покажет клавиатуру с кнопками
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    if message.text == "/start":
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
        bot.send_sticker(message.chat.id, choice_sticker())

    elif message.text.lower() == "погода":
        keyboard = tb.types.InlineKeyboardMarkup(row_width=2)
        item1 = tb.types.InlineKeyboardButton("Новосибирск", callback_data='Nsk')
        item2 = tb.types.InlineKeyboardButton("Другой город", callback_data='Other')
        keyboard.add(item1, item2)

        bot.send_message(message.chat.id, "Где смотрим погоду?", reply_markup=keyboard)
    elif message.text.lower() == "прогноз":
        pass
    elif message.text.lower() == "курс":
        pass
    else:                                          # Повторяет сообщение в ответ
        bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Nsk':
                answer = get_weather('Novosibirsk')
                bot.send_message(call.message.chat.id, answer)
            elif call.data == 'Other':
                bot.send_message(call.message.chat.id, 'Бывает')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Погода", reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# Бот при получении стикера печатает информацию о сообщении,
# в конце параметр file_id это id стикера, можно использовать
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    print(message.sticker.file_id)


def choice_sticker():
    sticker_list = ['CAACAgIAAxkBAAN3XrgwD1zIwYTS7Qm5EUZr8mg18OIAAiQDAAK1cdoGn4orPORRz70ZBA',
                    'CAACAgIAAxkBAAN4XrgwLZoCP50lj3abQeACdgeq2sUAAiUDAAK1cdoGfJufVdtFLjIZBA',
                    'CAACAgIAAxkBAAN5XrgwOmOEPXozC70h2DMuoSGr2swAAiYDAAK1cdoGPhkLi-ccGUAZBA',
                    'CAACAgIAAxkBAAN6Xrgwm3aYpUr20O6nV_br6ILxmQEAAicDAAK1cdoGD_Tez6DF3ewZBA',
                    'CAACAgIAAxkBAAN7XrgwrrtZIUWFxAi221Ftjs3c8w4AAigDAAK1cdoGkHpKh16VSm4ZBA',
                    'CAACAgIAAxkBAAN8Xrgwsw60DI1VaxWan5Xbg-mb1HIAAikDAAK1cdoG3TGSJ5vexAEZBA',
                    'CAACAgIAAxkBAAN9XrgwtGH8v7Zatq5tafdsQxDTLrEAAioDAAK1cdoG4UpwRi3ZAAEOGQQ',
                    'CAACAgIAAxkBAAN-XrgwtdQJ8uyzjUCOYKI2UmxjxewAAisDAAK1cdoGt5DSzMyC4jUZBA',
                    'CAACAgIAAxkBAAN_Xrgwtloie0FwYlxMGAw6qprm-RwAAiwDAAK1cdoGi2CX4OHQH3UZBA',
                    'CAACAgIAAxkBAAOAXrgwt28D-KcXh81hbovigTJ2zgIAAi0DAAK1cdoGUl1IOjgOloAZBA',
                    'CAACAgIAAxkBAAOBXrgwub0UqiLERdq1kvEe48bBw9gAAi4DAAK1cdoGqijNuZzJUrYZBA',
                    'CAACAgIAAxkBAAOCXrgwutFc0gghAiGlbSGDQynb9XEAAi8DAAK1cdoG7QUwS7ZjTdEZBA',
                    'CAACAgIAAxkBAAODXrgwu-WKVuT6FxMnsoYdpWuIDDwAAjADAAK1cdoGcRM5b76mxq0ZBA',
                    'CAACAgIAAxkBAAMvXrfANPopMDaRS1Q1Zy3jAAEvqNxyAAIxAwACtXHaBqKdXuJ4Jm7mGQQ',
                    'CAACAgIAAxkBAAOEXrgw9tkjDUrVCXvs9Qk_k_a4IHMAAjIDAAK1cdoGvMw2Lq6YsJkZBA',
                    'CAACAgIAAxkBAAOFXrgw-O4Q6WPfoIEfpfHwY70KbEwAAjMDAAK1cdoGjOgtjpKnM-gZBA',
                    'CAACAgIAAxkBAAOGXrgw-EYCE3cHC7nPIQgGsHvVgUsAAjUDAAK1cdoGaH3DKjMQpgIZBA',
                    'CAACAgIAAxkBAAOHXrgw-WGA7x8BDfZMVp0nydNt83QAAjYDAAK1cdoGIO6VI_OQQDYZBA',
                    'CAACAgIAAxkBAAOIXrgw-huAwELQ3xcfyxF2cxEwYQMAAjcDAAK1cdoGpICR6sb4aHYZBA',
                    'CAACAgIAAxkBAAOJXrgw-gWvqzsBFh2eBqFpKCTrV5sAAjgDAAK1cdoGwvLeWs_qDRUZBA',
                    'CAACAgIAAxkBAAOKXrgw_Na0SELuGGb1IuwXjk1UxKcAAjkDAAK1cdoGI1BmZ7xGOK0ZBA',
                    'CAACAgIAAxkBAAOLXrgw_TgOBjCnvt8EeUFg4eX8m2kAAjoDAAK1cdoG7ojNiCeYrAwZBA',
                    'CAACAgIAAxkBAAOMXrgw_T_2QdyYsKBkt5T9uCaoHesAAjsDAAK1cdoGGEsG0lVTy0QZBA',
                    'CAACAgIAAxkBAAONXrgw_lMRXiyvEQ1dZoP2pg55PAYAAjwDAAK1cdoGJSoa62i0WYwZBA',
                    'CAACAgIAAxkBAAOOXrgw_xLlN-I5_FgCCotXem2NOFoAAj0DAAK1cdoGr9sW6YezqqEZBA']
    return choice(sticker_list)


def get_weather(place):
    weath_dict = getw.weather(place)
    str0 = place + "\n"
    str1 = "Температура: {0} C\nВлажность: {1}%\n".format(str(weath_dict['temperature']),
                                                          str(weath_dict['humidity']))
    str2 = "Давление {0} мм.рт.ст\nВетер: {1} м/с\n".format(str(round(weath_dict['pressure'] / 1.33322, 1)),
                                                            str(weath_dict['wind']))
    str3 = "UV-индекс: {0}\nUV-риск: {1}\n".format(str(weath_dict['uv_val']),
                                                   str(weath_dict['uv_risk']))
    return str1 + str2 + str3


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([tb.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://young-hamlet-55059.herokuapp.com/bot")
    return "?", 200

# bot.polling()


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
