import telebot
from session_key_generator import gen_session_key
import DataBase as db

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

        session_number = gen_session_key()
        db.add_session(session_number)
        db.add_player(call.from_user.id)
        db.add_player_to_session(call.from_user.id, session_number)
        createGameMessage = f'Игрокам нужно присоединиться по номеру: {session_number}'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                              reply_markup=reply_markup)
    elif call.data == "Join":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Authors":
        print(call.from_user)
        pass
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    # call.data для создания сессии
    elif call.data == "Round_Length":
        keyboard = [
            [telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Round_10'),
             telebot.types.InlineKeyboardButton("30", callback_data='Time_For_Round_30'),
             telebot.types.InlineKeyboardButton("45", callback_data='Time_For_Round_45')],
            [telebot.types.InlineKeyboardButton("60", callback_data='Time_For_Round_60'),
             telebot.types.InlineKeyboardButton("90", callback_data='Time_For_Round_90')]
        ]
        reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
        round_length_text = 'Выберите длительность раунда (в секундах)'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)
    elif call.data == "Dictionary":
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
        pass
    elif call.data == "Start_Game":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Time_For_Round_10":
        session_number = db.get_from_player(call.from_user.id)
        # db.change_time(session_number, 10)
        # return callback_query("Create_Game"
        # bot.answer_callback_query()
        # callback_data("Create_Game")
        # print(call)
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        #                       text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)
        # telebot(call, callback_data="Create_Game")
    # elif call.data == "Time_For_Round_30":
    #     session_number = db.get_from_player(call.from_user.id)
    #     db.change_time(session_number, 30)
    # elif call.data == "Time_For_Round_45":
    #     session_number = db.get_from_player(call.from_user.id)
    #     db.change_time(session_number, 45)
    # elif call.data == "Time_For_Round_60":
    #     session_number = db.get_from_player(call.from_user.id)
    #     db.change_time(session_number, 60)
    # elif call.data == "Time_For_Round_90":
    #     session_number = db.get_from_player(call.from_user.id)
    #     db.change_time(session_number, 90)

# @bot.message_handler(callback_data='1')
# def handle_all_message(message):
#     bot.send_message(message, message.text)


bot.polling()
