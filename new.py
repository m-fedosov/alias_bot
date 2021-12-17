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
        [telebot.types.InlineKeyboardButton("Поехали", callback_data='Create_Game'+'$'+new_key)]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Суть игры заключается в объяснении слов с помощью синонимов, '
                                      'антонимов или подсказок. Игрокам необходимо обьяснить как можно '
                                      'больше слов за отведенный период времени. За каждое отгаданное слово '
                                      'игроки получают 1 очко и продвигаются на 1 шаг вперед. Для победы нужно '
                                      'набрать больше 24 очков', reply_markup=reply_markup, parse_mode="HTML")



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    if "Create_Game" in call.data:
        create_game(call)
    elif "Round_Length" in call.data:
        round_length(call)
    elif "Start_Game" in call.data:
        game(call)
    elif "YES" in call.data:
        cur_session = sessions[call.data[-4:]]
        if 'guessed' in call.data:
            resp = cur_session.next_team(1)
            if resp == 1:
                game(call)
            elif resp == 3:
                game_end(call)
            else:
                round(call)
        elif 'passed' in call.data:
            resp = cur_session.next_team(0)
            if resp == 1:
                game(call)
            elif resp == 3:
                game_end(call)
            else:
                round(call)
        else:
            round(call)


    elif "Time_For_Round_10" in call.data:
        sessions[call.data[-4:]].change_time(3)
        print(sessions)
    elif "Time_For_Round_30" in call.data:
        sessions[call.data[-4:]].change_time(5)
        print(sessions)
    elif "Time_For_Round_45" in call.data:
        sessions[call.data[-4:]].change_time(10)
        print(sessions)
    elif "Time_For_Round_60" in call.data:
        sessions[call.data[-4:]].change_time(60)
        print(sessions)
    elif "Time_For_Round_90" in call.data:
        sessions[call.data[-4:]].change_time(90)
        print(sessions)
    elif "Teams" in call.data :
        change_teams(call)
    elif 'Супер коровы' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'Псы Волколаки' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'Ночные Бабушки' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(call.data)
        print(sessions)
    elif 'Биполярные Медведи' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'Лягушки в обмороке' in call.data:
        sessions[call.data[-4:]].add_team((call.data)[:-5])
        print(sessions)
    elif 'End_Game' in call.data:
        thanks(call)
    elif 'Next_Game' in call.data:
        cur_session = sessions[call.data[-4:]]
        cur_session.clear()
        create_game(call)
    elif 'Authors' in call.data:
        authors(call)
    elif 'after_authors' in call.data:
        game_end(call)


def create_game(call):

    new_key = call.data[-4:]

    keyboard = [
        [telebot.types.InlineKeyboardButton("Длительность раунда", callback_data='Round_Length'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Начать игру", callback_data='Start_Game'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Добавить команды", callback_data='Teams'+'$'+new_key)]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    #createGameMessage = 'легендарная хуйня'
    createGameMessage = 'параметры'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)

def game(call):

    cur_session = sessions[call.data[-4:]]
    cur_team = cur_session.cur_team()
    keyboard = [
        [telebot.types.InlineKeyboardButton("Да!", callback_data='YES' + '$' + call.data[-4:])]
    ]
    #print(cur_team)
    ready = f'Команда {str(cur_team)}, вы готовы?\nОчко команд:\n'
    for i in cur_session.teams:
        ready += (' ' + str(i.name) + ' ' + str(i.points) + '\n')
    #print(ready)
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=ready,
                          reply_markup=reply_markup)



def round(call):
    cur_session = sessions[call.data[-4:]]
    word = cur_session.give_word()
    keyboard = [
        [telebot.types.InlineKeyboardButton("Отгадано", callback_data='YES_guessed' + '$' + call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Пропущено", callback_data='YES_passed' + '$' + call.data[-4:])]
    ]
    #print(cur_session)
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=  "ваше слово: "+word,
                          reply_markup=reply_markup)



def round_length(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("3", callback_data='Time_For_Round_10'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("5", callback_data='Time_For_Round_30'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Round_45'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("60", callback_data='Time_For_Round_60'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("90", callback_data='Time_For_Round_90'+'$'+call.data[-4:])]
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    round_length_text = 'Выберите длительность раунда (в секундах)'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)


def change_teams(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Супер коровы", callback_data='Супер коровы'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Псы Волколаки", callback_data='Псы Волколаки'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Ночные Бабушки", callback_data='Ночные Бабушки'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Биполярные Медведи", callback_data='Биполярные Медведи' + '$' + call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Лягушки в обмороке", callback_data='Лягушки в обмороке' + '$' + call.data[-4:])],

    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    teams_text = 'нажмите на названия команд, которые хотите добавить'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=teams_text, parse_mode="HTML", reply_markup=reply_markup)


def game_end(call):
    
    cur_session = sessions[call.data[-4:]]

    keyboard = [
        [telebot.types.InlineKeyboardButton("Новая игра", callback_data='Next_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Завершить игру", callback_data='End_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Авторы", callback_data='Authors'+'$'+call.data[-4:])]
    ]

    text_endgame = 'Игра завершена, победила команда команда\n'
    text_endgame += 'Очко команд:\n'
    for i in cur_session.teams:
        text_endgame += (' ' + str(i.name) + ' ' + str(i.points) + '\n')
    
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text_endgame, parse_mode="HTML", reply_markup=reply_markup)


def authors(call):
    keyboard = [
        [telebot.types.InlineKeyboardButton("Панаятна", callback_data='after_authors' +'$' +call.data[-4:])],
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    createGameMessage = 'Авторы рукожопы и ленятий ничего делать не умеют, на звания пРоГрАмМиСтОв не претендуют'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)


# def next_game(call):
#     cur_session = sessions[call.data[-4:]]




def thanks(call):
    cur_session = sessions[call.data[-4:]]
    cur_session.clear()
    text = "Спасибо за игру"
    keyboard = [[]]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, parse_mode="HTML", reply_markup=reply_markup)

#bot.polling()
bot.infinity_polling()
