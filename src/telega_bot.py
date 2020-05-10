import telebot as tb
import config
import getweather as getw

# Создаем бота
bot = tb.TeleBot(config.TELEGRAM)


# Если послать боту комманду /start
# то отправит сообщение и покажет клавиатуру с кнопками
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, "Офигенски, погнали!")
    elif message.text == "/help":
        bot.send_message(message.chat.id, "HELP в разработке")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "привет":           # Отвечает на сообщение
        bot.send_message(message.chat.id, "Привет, создатель!")

    elif message.text.lower() == "мощно":          # Отправляет стикер в ответ  на сообщение
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMvXrfANPopMDaRS1Q1Zy3jAAEvqNxyAAIxAwACtXHaBqKdXuJ4Jm7mGQQ')

    elif message.text.lower() == "погода":
        print("Погода")

        keyboard = tb.types.InlineKeyboardMarkup(row_width=2)
        item1 = tb.types.InlineKeyboardButton("Новосибирск", callback_data='Nsk')
        item2 = tb.types.InlineKeyboardButton("Другой город", callback_data='Other')
        keyboard.add(item1, item2)

        bot.send_message(message.chat.id, "Где смотрим погоду?", reply_markup=keyboard)

    # else:                                          # Повторяет сообщение в ответ
    #     bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Nsk':
                get_weather('Novosibirsk')
                bot.send_message(call.message.chat.id, 'Вот и отличненько')
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
    print(message)


def get_weather(place):
    pass


bot.polling()
