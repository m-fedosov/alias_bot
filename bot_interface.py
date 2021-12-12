import telebot

bot = telebot.TeleBot("5036774816:AAHchvlUTJaraZVF0YjQU45x0PviPkweH8I", parse_mode="MarkdownV2")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [telebot.types.InlineKeyboardButton("Создать игру", callback_data='1')],
        [telebot.types.InlineKeyboardButton("Присоединиться", callback_data='2')],
        [telebot.types.InlineKeyboardButton("Авторы", callback_data='3')]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, ' Суть игры заключается в объяснении слов с помощью синонимов,'
                                      ' антонимов или подсказок. Игрокам необходимо обьяснить как можно '
                                      'больше слов за отведенный период времени. За каждое отгаданное слово '
                                      'игроки получают 1 очко и продвигаются на 1 шаг вперед. Для победы нужно '
                                      'набрать больше 24 очков', reply_markup=reply_markup, parse_mode="HTML")


# @bot.message_handler(func=lambda message: True)
# def handle_all_message(message):
#     bot.send_message('', message.text)



bot.polling()