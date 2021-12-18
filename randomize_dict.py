
import numpy as np

def randomize_dict():
    ''' 
    Возвращает массив с перемешанными в случайном порядке словами
    Не принимает ничего на вход, возвращает перемешанный уникальный словарь 
    '''
    dict_from_file = []
    with open('words.txt', 'r', encoding = 'UTF-8') as file:
        for i in file:
            dict_from_file.append(i.rstrip())
    
    unique_dict = []
    order = np.arange(len(dict_from_file))
    np.random.shuffle(order)
    for i in order:
        unique_dict.append(dict_from_file[i])

    return unique_dict

