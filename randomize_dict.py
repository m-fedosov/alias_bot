#import random
import numpy as np

''' Возвращает массив с перемешанными в случайном порядке словами'''

def randomize_dict():
    
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

