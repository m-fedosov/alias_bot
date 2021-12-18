import random


def gen_session_key():
    """
    Генерирует уникальный ключ сессии\n
    Не принимает ничего на вход, возвращает уникальный случайный ключ сессии, состоящий из щаглавных букв английского алфавита и цифр
    """
    a = [chr(i) for i in range(65, 90)] + [str(i) for i in range(10)]
    session_key = ''
    for i in range(4):
        session_key += random.choice(a)
    return session_key


