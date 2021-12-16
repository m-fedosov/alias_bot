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
        create_game(call)
    elif call.data == "Authors":
        print(call.from_user)
        pass
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    # call.data для создания сессии
    elif call.data == "Round_Length":
        round_length(call)
    elif call.data == "Join":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Start_Game":

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='')
    elif call.data == "Time_For_Round_10":
        change_length_session(10, call)
    elif call.data == "Time_For_Round_30":
        change_length_session(30, call)
    elif call.data == "Time_For_Round_45":
        change_length_session(45, call)
    elif call.data == "Time_For_Round_60":
        change_length_session(60, call)
    elif call.data == "Time_For_Round_90":
        change_length_session(90, call)


def create_game(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("Длительность раунда", callback_data='Round_Length')],
        [telebot.types.InlineKeyboardButton("Начать игру", callback_data='Start_Game')]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    try:
        session_number = db.get_from_player(call.from_user.id)
    except:
        session_number = gen_session_key()
        db.add_session(session_number)
        db.add_player(call.from_user.id)
        db.add_player_to_session(call.from_user.id, session_number)
    createGameMessage = f'Игрокам нужно присоединиться по номеру: {session_number}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)


def join_game(call):



def start_game(call):
    alias_speaker = ''
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=seconds_text, parse_mode="HTML", reply_markup=reply_markup)

def round_length(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Round_10'),
         telebot.types.InlineKeyboardButton("30", callback_data='Time_For_Round_30'),
         telebot.types.InlineKeyboardButton("45", callback_data='Time_For_Round_45')],
        [telebot.types.InlineKeyboardButton("60", callback_data='Time_For_Round_60'),
         telebot.types.InlineKeyboardButton("90", callback_data='Time_For_Round_90')]
    ]
    print(keyboard)
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    round_length_text = 'Выберите длительность раунда (в секундах)'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)


def change_length_session(sec, call):
    session_number = db.get_from_player(call.from_user.id)
    db.change_time(session_number, sec)
    keyboard = [[telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'),
                telebot.types.InlineKeyboardButton("изменить", callback_data='Round_Length')]]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    seconds_text = f'Длительность раунда {sec} секунд'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=seconds_text, parse_mode="HTML", reply_markup=reply_markup)


bot.polling()
