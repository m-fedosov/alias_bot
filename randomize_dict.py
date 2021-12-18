import random

def randomize_dict():
    ''' 
    Возвращает массив с перемешанными в случайном порядке словами
    Не принимает ничего на вход, возвращает перемешанный уникальный словарь 
    '''
    dict_from_file = []
    with open('words.txt', 'r', encoding = 'UTF-8') as file:
        for i in file:
            dict_from_file.append(i.rstrip())
    random.shuffle(dict_from_file)
    return dict_from_file
