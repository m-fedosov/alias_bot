import telebot

bot = telebot.TeleBot("5036774816:AAHchvlUTJaraZVF0YjQU45x0PviPkweH8I", parse_mode="MarkdownV2")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [telebot.types.InlineKeyboardButton("Создать игру", callback_data='Create_Game')],
        [telebot.types.InlineKeyboardButton("Присоединиться", callback_data='Join')],
        [telebot.types.InlineKeyboardButton("Авторы", callback_data='Authors')]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Суть игры заключается в объяснении слов с помощью синонимов, '
                                      'антонимов или подсказок. Игрокам необходимо обьяснить как можно '
                                      'больше слов за отведенный период времени. За каждое отгаданное слово '
                                      'игроки получают 1 очко и продвигаются на 1 шаг вперед. Для победы нужно '
                                      'набрать больше 24 очков', reply_markup=reply_markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Create_Game":
        keyboard = [
            [telebot.types.InlineKeyboardButton("Длительность раунда", callback_data='Round_Length'),
             telebot.types.InlineKeyboardButton("Словарь", callback_data='Dictionary')],
            [telebot.types.InlineKeyboardButton("Начать игру", callback_data='Start_Game')]
        ]

        reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

        session_number = 666
        createGameMessage = f'Игрокам нужно присоединиться по номеру: {session_number}'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                              reply_markup=reply_markup)
    elif call.data == "Join":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Authors":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    # call.data для создания сессии
    elif call.data == "Round_Length":
        keyboard = [
            [telebot.types.InlineKeyboardButton("10", callback_data='Create_Game'),
             telebot.types.InlineKeyboardButton("30", callback_data='Create_Game'),
             telebot.types.InlineKeyboardButton("45", callback_data='Create_Game')],
            [telebot.types.InlineKeyboardButton("60", callback_data='Create_Game'),
             telebot.types.InlineKeyboardButton("90", callback_data='Create_Game')]
        ]
        reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
        round_length_text = 'Введите длительность раунда или выберите из предложенных (в секундах)'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)
    elif call.data == "Dictionary":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Start_Game":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')


# @bot.message_handler(callback_data='1')
# def handle_all_message(message):
#     bot.send_message(message, message.text)


bot.polling()
