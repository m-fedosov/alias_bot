from tinydb import TinyDB, Query
from tinydb.operations import increment, add
from randomize_dict import randomize_dict
from new_rand_dict import get_rand_dict
import numpy as np


class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0


class Session:
    def __init__(self, key):
        self.teams = []

        with open("words.txt", encoding='utf-8') as file:
            self.dictionary = [i[:len(i) - 1] for i in file]
        self.key = key
        self.counter = 0
    def give_word(self):
        ret = self.dictionary[self.counter]
        self.counter += 1
        return ret
    def add_team(self,team : Team):
        self.teams.append(team)

    def clear(self):
        self.key = ''
        self.teams = []
        self.dictionary = []
        self.counter = 0











def add_session(key='', lst=[], time=60):
    """
    Добавляет сессию в бд

    :param key: ключ сессии
    :param cnt: кол-во игроков
    :param lst: список игроков, в списке хранятся id игроков
    :return:
    """
    db = TinyDB('db.json')
    db.insert(
        {'type': 'session',
         'key': key,
         'time_for_round': 60,
         'list_of_teams': lst,
         'i': [i for i in range(500)],
         'dictionary': zip([i for i in range(500)],get_rand_dict(500)),# получил список длинной 500 из чисел от 0 до 1000 (номера слов)
         }
    )


def add_team(key = '', team_name=''):
    db = TinyDB('db.json')
    db.update(add('list_of_teams',[team_name]),Query().key == key)

def get_word_num(key =''):
    db = TinyDB('db.json')
    ret = get_from_session()

def add_player_to_session(player_id=0, session_key=0):
    """
    Добавляет игрока к сессии

    :param player_id: id игрока
    :param session_key: ключ сессии
    """
    db = TinyDB('db.json')
    db.update(add('list_of_players', [player_id]), Query().key == session_key)
    db.update({'curent_session':session_key},Query().id == player_id)




# def add_player(id=0, name='Petux'):
#     """
#     Добавляет игрока в бд

#     :param id: уникальный id игрока
#     :return:
#     """
#     db = TinyDB('db.json')
#     if db.search(Query().id == id) == []:
#         db.insert(
#             {
#                 'type': 'player',
#                 'name': name,
#                 'curent_session': -1,
#                 'id': id,
#                 'score': 0
#             }
#         )
#     else:
#         print("Уже есть игрок с id", id)


def clear():
    """
    очистить базу
    """
    db = TinyDB('db.json')
    db.truncate()

def score_up(player_id,value=1):
    """
    Изменитть кол-во очков игрока

    :param player_id: id игрока
    :param value: кол-во добавленных очков
    :return:
    """
    db = TinyDB('db.json')
    if db.search(Query().id == player_id) != []:
        db.update(add('score',value),Query().id == player_id)

    
def change_time(key = '',new_time = 60):
    """
    Поменять время в сессии

    :param key: ключ сессии, в  которой меняешь время
    :param new_time: новое время
    :return:
    """
    db = TinyDB('db.json')
    if db.search(Query().key == key)!= []:
        db.update({'time_for_round' : new_time},Query().key == key)

def add_dictionary(key = ''):
    with open ('words.txt', 'r', encoding="UTF-8") as file:
        db = TinyDB('db.json')
        db.update({'dictionary': randomize_dict()}, Query().key == key)

def word_from_dict(session_number, num_of_word = 0):
    next_word = (get_from_session(key=session_number, take='dictionary'))[num_of_word]
    return next_word

def get_from_player(id = 0, take = 'curent_session'):
    """
    вытащить параметр с игрока
    """

    db = TinyDB('db.json')
    if db.search(Query().id == id) != []:
        return db.search(Query().id == id)[0][take]

def get_from_session(key ='', take = 'list_of_players'):
    """
    вытащить параметр из сессии
    """
    db = TinyDB('db.json')
    return db.search(Query().key == key)[0][take]

def next_alias_answering(session_num, next_pl=0, take = 'order_player'):
    
    db = TinyDB('db.json')
    next_player = db.search(Query().key == session_num)[0][take] 
    return next_player







# clear()
# add_player(1,"Serik")
# add_player(2,"Goga")
# add_player(3,'Kuka')
# add_player(3,'asdads')
# add_session('first')
# add_player_to_session(1,'first')
# add_player_to_session(2,'first')
# add_player_to_session(2,'first')
# add_player_to_session(2,'first')
# add_player_to_session(3,'first')
# score_up(1)
# score_up(1)
# score_up(2)
