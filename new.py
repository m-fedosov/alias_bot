import telebot
from session_key_generator import gen_session_key
#import DataBase as db
import new_db as db

bot = telebot.TeleBot("5036774816:AAHchvlUTJaraZVF0YjQU45x0PviPkweH8I", parse_mode="MarkdownV2")

sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Sends a message with three inline buttons attached."""
    
    new_key=gen_session_key()
    new_session = db.Session(new_key)
    sessions[new_key] = new_session

    
    keyboard = [
        [telebot.types.InlineKeyboardButton("Поехали", callback_data='Create_Game'+'$'+new_key)],
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Суть игры заключается в объяснении слов с помощью синонимов, '
                                      'антонимов или подсказок. Игрокам необходимо обьяснить как можно '
                                      'больше слов за отведенный период времени. За каждое отгаданное слово '
                                      'игроки получают 1 очко и продвигаются на 1 шаг вперед. Для победы нужно '
                                      'набрать больше 24 очков', reply_markup=reply_markup, parse_mode="HTML")


# @bot.message_handler(content_types=['text'])
# def get_session(message):
#     session = message.text
#     session = session.upper()
#     db.add_player(message.from_user.id, message.from_user.username)
#     db.add_player_to_session(message.from_user.id, session)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if "Create_Game" in call.data:
        create_game(call)
    # elif call.data == "Authors":
    #     print(call.from_user)
    #     pass
    elif "Round_Length" in call.data:
        round_length(call)
    # elif call.data == "Join":
    #     join_game(call)
    elif call.data == "Start_Game":
        play_game(call)
    elif "Time_For_Round_10" in call.data:
        sessions[call.data[-4:]].change_time(10)
        print(sessions)
        # change_length_session(10, call)
    elif "Time_For_Round_30" in call.data:
        sessions[call.data[-4:]].change_time(30)
        print(sessions)
    elif "Time_For_Round_45" in call.data:
        sessions[call.data[-4:]].change_time(45)
        print(sessions)
    elif "Time_For_Round_60" in call.data:
        sessions[call.data[-4:]].change_time(60)
        print(sessions)
    elif "Time_For_Round_90" in call.data:
        sessions[call.data[-4:]].change_time(90)
        print(sessions)
    elif "Teams" in call.data :
        change_teams(call)
    elif 'Super_Cows' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'Were_Wolves' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'Night_Grans' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)

def create_game(call):
    
    new_key = call.data[-4:]
    # new_key=gen_session_key()
    # new_session = db.Session(new_key)
    # sessions[new_key] = new_session

    keyboard = [
        [telebot.types.InlineKeyboardButton("Длительность раунда", callback_data='Round_Length'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Начать игру", callback_data='Start_Game')],
        [telebot.types.InlineKeyboardButton("Добавить команды (по умолчанию две)", callback_data='Teams'+'$'+new_key)]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    createGameMessage = 'легендарная хуйня'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)
    #if call.data ==


# def join_game(call):
#      input_session = 'Введите номер сессии:'
#      bot.register_next_step_handler(bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                            text=input_session, parse_mode="HTML"), get_session)


def play_game(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("Вперёд", callback_data='round')],

    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

    session_number = db.get_from_player(call.from_user.id)

    index = 0#(db.get_from_session(key = session_number)).index(call.from_user.id)
    print(index)
    alias_word = db.word_from_dict(session_number, index)
    index+=1
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                        text=alias_word, parse_mode="HTML", reply_markup=reply_markup)
    
#import time
#import new_db as db

# def round(call,round_time,key):
#     st= time.perf_counter()
#     order_words = db.get_from_session(key,'order_words')
#     i = 0
#     keyboard = [
#         [telebot.types.InlineKeyboardButton("отгадано", callback_data='otgadano')],
#         [telebot.types.InlineKeyboardButton("пропустить", callback_data='pass')]
#     ]
#     while st - time.perf_counter() < 60.0:
#         if call.data == 'otgadano':
#             db =



def round_length(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Round_10'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("30", callback_data='Time_For_Round_30'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("45", callback_data='Time_For_Round_45'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("60", callback_data='Time_For_Round_60'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("90", callback_data='Time_For_Round_90'+'$'+call.data[-4:])]
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    round_length_text = 'Выберите длительность раунда (в секундах)'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)


# def change_length_session(sec, call):
#     session_number = db.get_from_player(call.from_user.id)
#     db.change_time(session_number, sec)
#     keyboard = [[telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'),
#                 telebot.types.InlineKeyboardButton("изменить", callback_data='Round_Length')]]
#     reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
#     seconds_text = f'Длительность раунда {sec} секунд'
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=seconds_text, parse_mode="HTML", reply_markup=reply_markup)

def change_teams(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Супер-коровы", callback_data='Super_Cows'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Псы-Волколаки", callback_data='Were_Wolves'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Ночные Бабушки", callback_data='Night_Grans'+'$'+call.data[-4:])],
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    teams_text = 'нажмите на названия команд, которые хотите добавить'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=teams_text, parse_mode="HTML", reply_markup=reply_markup)


    # msg = bot.send_message(chat_id=call.message.chat.id, reply_to_message_id=call.message.message_id,
    #                       text=teams_text, parse_mode="HTML")
    # bot.register_next_step_handler(msg.msg, create_game) # reply_markup=reply_markup), create_game)

def successfully_added_teams(call):
    keyboard = [[telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game')]]

bot.polling()