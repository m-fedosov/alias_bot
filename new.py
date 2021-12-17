import telebot
from session_key_generator import gen_session_key
#import DataBase as db
import new_db as db

bot = telebot.TeleBot("5036774816:AAHchvlUTJaraZVF0YjQU45x0PviPkweH8I", parse_mode="MarkdownV2")

sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Отправляет приветственное сообщение с единственной кнопкой, которая запускает игру.\n 
    В функции генерируется ключ сессии.
    """
    
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
    """
    Данная функция отвечает за кнопки, появляющиеся на различных этапах игры
    """
    
    if "Create_Game" in call.data:
        create_game(call)
    elif "Round_Length" in call.data:
        round_length(call)
    elif "Game_Length" in call.data:
        game_length(call)
    elif "Start_Game" in call.data:
        cur_session = sessions[call.data[-4:]]
        if len(cur_session.teams) >= 1:
            game(call)
        else:
            error_teams(call)
    ##############################################
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
    ###############################################
    elif "Time_For_Round_3" in call.data:
        sessions[call.data[-4:]].change_time(3)
        print(sessions)
    elif "Time_For_Round_5" in call.data:
        sessions[call.data[-4:]].change_time(5)
        print(sessions)
    elif "Time_For_Round_10" in call.data:
        sessions[call.data[-4:]].change_time(10)
        print(sessions)
    elif "Time_For_Round_15" in call.data:
        sessions[call.data[-4:]].change_time(15)
        print(sessions)
    elif "Time_For_Round_50" in call.data:
        sessions[call.data[-4:]].change_time(50)
        print(sessions)
    ###############################################
    elif "Time_For_Game_10" in call.data:
        sessions[call.data[-4:]].change_max_score(10)
        print(sessions)
    elif "Time_For_Game_20" in call.data:
        sessions[call.data[-4:]].change_max_score(20)
        print(sessions)
    elif "Time_For_Game_30" in call.data:
        sessions[call.data[-4:]].change_max_score(30)
        print(sessions)
    elif "Time_For_Game_50" in call.data:
        sessions[call.data[-4:]].change_max_score(50)
        print(sessions)
    elif "Time_For_Game_100" in call.data:
        sessions[call.data[-4:]].change_max_score(100)
        print(sessions)
    ################################################
    elif "Teams" in call.data :
        change_teams(call)
    elif 'Супер Коровы' in call.data:
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
    ###########################################################
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
    """
    Функция отвечает за этап игры, на котором человек вводит длительность игры, длительность раунда, добавляет команды, а также начинает игру
    """
    new_key = call.data[-4:]
    cur_session = sessions[new_key]
    cur_teams = cur_session.teams
    keyboard = [
        [telebot.types.InlineKeyboardButton("Начать игру", callback_data='Start_Game'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Длительность раунда", callback_data='Round_Length'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Длительность игры", callback_data='Game_Length'+'$'+new_key)],
        [telebot.types.InlineKeyboardButton("Добавить команды", callback_data='Teams'+'$'+new_key)]
    ]

    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    #createGameMessage = 'легендарная хуйня'
    createGameMessage = 'Выберите подходящие параметры для своей игры, затем нажмите "Начать игру", чтобы к ней присоединиться\n'
    createGameMessage += cur_session.get_info()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)

def game(call):
    """
    Функция изменяет сообщение на 'Вы готовы?', показывает отвечающую команду и и её очки
    """
    cur_session = sessions[call.data[-4:]]
    cur_team = cur_session.cur_team()
    keyboard = [
        [telebot.types.InlineKeyboardButton("Да!", callback_data='YES' + '$' + call.data[-4:])]
    ]
    #print(cur_team)
    ready = f'Команда {str(cur_team)}, вы готовы?\nОчки команд:\n'
    for i in cur_session.teams:
        ready += (' ' + str(i.name) + ' ' + str(i.points) + '\n')
    #print(ready)
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=ready,
                          reply_markup=reply_markup)


def round(call):
    """
    Функция отвечает за раунд в игре, изменяет сообщение, показывая новое слово, под которым имеются кнопки "Отгадано" и "Пропущено"
    """
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
    """
    Функция изменяет сообщение, показывая кнопки, через которые можно изменить количество слов, которое будет объяснять команда в раунде
    """
    keyboard = [
        [telebot.types.InlineKeyboardButton("3", callback_data='Time_For_Round_3'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("5", callback_data='Time_For_Round_5'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Round_10'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("15", callback_data='Time_For_Round_15'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("50", callback_data='Time_For_Round_50'+'$'+call.data[-4:])]
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    round_length_text = 'Выберите длительность раунда (количество слов, объясняемое за раунд)'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)

def game_length(call):
    """
    Функция изменяет сообщение, показывая кнопки, через которые можно изменить количество слов, требуемое для победы в игре
    """
    keyboard = [
        [telebot.types.InlineKeyboardButton("10", callback_data='Time_For_Game_10'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("20", callback_data='Time_For_Game_20'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("30", callback_data='Time_For_Game_30'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("50", callback_data='Time_For_Game_50'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:]),
         telebot.types.InlineKeyboardButton("100", callback_data='Time_For_Game_100'+'$'+call.data[-4:])]
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    round_length_text = 'Выберите длительность игры (в количестве слов)'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=round_length_text, parse_mode="HTML", reply_markup=reply_markup)

def change_teams(call):
    """
    Функция изменяет сообщение, показывая кнопки, через которые можно изменить команды, участвующие в игре
    """
    cur_session = sessions[call.data[-4:]]
    
    keyboard = [
        [telebot.types.InlineKeyboardButton("ОК", callback_data='Create_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Супер Коровы 🐮" + '✅' if "🐮" in cur_session.get_info() else "Супер Коровы 🐮" + '', callback_data='Супер Коровы'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Псы Волколаки 🐺" + '✅' if "🐺" in cur_session.get_info() else "Псы Волколаки 🐺" + '', callback_data='Псы Волколаки'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Ночные Бабушки 👵" + '✅' if "👵" in cur_session.get_info() else "Ночные Бабушки 👵" + '', callback_data='Ночные Бабушки'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Биполярные Медведи 🐼" + '✅' if "🐼" in cur_session.get_info() else "Биполярные медведи 🐼" + '', callback_data='Биполярные Медведи' + '$' + call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Лягушки в обмороке 🐸" + '✅' if "🐸" in cur_session.get_info() else "Лягушки в обмороке 🐸" + '', callback_data='Лягушки в обмороке' + '$' + call.data[-4:])],

    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    teams_text = 'нажмите на названия команд, которые хотите добавить'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=teams_text, parse_mode="HTML", reply_markup=reply_markup)


def game_end(call):
    """
    Функция изменяет сообщение в конце игры, показывая кнопки, с помощью которых можно начать новую игру, завершить игру и посмотреть на авторов
    """
    cur_session = sessions[call.data[-4:]]

    keyboard = [
        [telebot.types.InlineKeyboardButton("Новая игра", callback_data='Next_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Завершить игру", callback_data='End_Game'+'$'+call.data[-4:])],
        [telebot.types.InlineKeyboardButton("Авторы", callback_data='Authors'+'$'+call.data[-4:])]
    ]

    text_endgame = 'Игра завершена, победила команда команда\n'
    text_endgame += 'Очки команд:\n'
    for i in cur_session.teams:
        text_endgame += (' ' + str(i.name) + ' ' + str(i.points) + '\n')
    
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text_endgame, parse_mode="HTML", reply_markup=reply_markup)


def authors(call):
    """
    Функция изменяет сообщение в конце игры, показывая информацию об авторах
    """
    keyboard = [
        [telebot.types.InlineKeyboardButton("Панаятна", callback_data='after_authors' +'$' +call.data[-4:])],
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    createGameMessage = 'Авторы рукожопы и ленятий ничего делать не умеют, на звания пРоГрАмМиСтОв не претендуют'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)

def error_teams(call):
    """
    Функция изменяет сообщение, показывая, что нельзя начать игру, если не была добавлена ни одна команда
    """
    keyboard = [
        [telebot.types.InlineKeyboardButton("Ладно(", callback_data='Create_Game' +'$' +call.data[-4:])],
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    createGameMessage = 'Вам необходимо добавить хотя бы одну команду👉👈'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=createGameMessage,
                          reply_markup=reply_markup)
                          
def thanks(call):
    """
    Функция отправляет сообщение с благодарностью за игру
    """
    cur_session = sessions[call.data[-4:]]
    cur_session.clear()
    text = "Спасибо за игру!"
    keyboard = [[]]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, parse_mode="HTML", reply_markup=reply_markup)

#bot.polling()
bot.infinity_polling()
