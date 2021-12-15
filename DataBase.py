from tinydb import TinyDB, Query
from tinydb.operations import increment, add



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
         'time_for_round': time,
         'step': 0,
         'list_of_players': lst
         }
    )




def add_player_to_session(player_id=0, session_key=0):
    """
    Добавляет игрока к сессии

    :param player_id: id игрока
    :param session_key: ключ сессии
    """
    db = TinyDB('db.json')
    if db.search(Query().id == player_id) == []:
        print("нет игрока с id",player_id)
        raise Exception
    if db.search(Query().key == session_key) == []:
        print("нет сессии с номером", session_key)
        raise ValueError
    db.update(add('list_of_players', [player_id]), Query().key == session_key)
    db.update({'curent_session':session_key},Query().id == player_id)



def add_player(id=0, name='Petux'):
    """
    Добавляет игрока в бд

    :param id: уникальный id игрока
    :return:
    """
    db = TinyDB('db.json')
    db.insert(
        {
            'type': 'player',
            'name': name,
            'curent_session': -1,
            'id': id,
            'score': 0
        }
    )


def clear():
    """
    очистить базу
    """
    db = TinyDB('db.json')
    db.truncate()

def score_up(player_id,value=1):
    """

    :param player_id: id игрока
    :param value: кол-во добавленных очков
    :return:
    """
    db = TinyDB('db.json')
    db.update(add('score',value),Query().id == player_id)
    
def change_time(key = '',new_time = 60):
    """
    Поменять время в сессии

    :param key: ключ сессии, в  которой меняешь время
    :param new_time: новое время
    :return:
    """
    db = TinyDB('db.json')
    db.update({'time_for_round' : new_time},Query().key == key)

def get_from_player(id = 0, take = 'curent_session'):
    """
    вытащить параметр
    """

    db = TinyDB('db.json')
    return db.search(Query().id == id)[0][take]

clear()
add_player(1,"Serik")
add_player(2,"Goga")
add_player(3,'Kuka')
add_session('first')
add_player_to_session(1,'first')
add_player_to_session(2,'first')
print(get_from_player(1))
score_up(1)
score_up(1)
score_up(2)
