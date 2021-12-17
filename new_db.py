from tinydb import TinyDB, Query
from tinydb.operations import increment, add
from randomize_dict import randomize_dict
from new_rand_dict import get_rand_dict
import numpy as np
import random


class Team:
    """
    Класс команды, хранит информацию о команде (название и набранные очки)
    """
    def __init__(self, name):
        """
        Конструктор

        :param name: название команды
        """
        self.name = name
        self.points = 0
    def __repr__(self) -> str:
        return str(self.name) + ' '+ str(self.points)


class Session:
    """
    Класс сессии, хранит информацию о сессии
    """
    def __init__(self, key):
        """
        Конструктор

        :param key: ключ сессии
        """
        self.teams = []

        # with open("words.txt", encoding='utf-8') as file:
        #     self.dictionary = ([i[:len(i) - 1] for i in file])
        self.dictionary = randomize_dict()
        self.key = key
        self.counter = 0
        self.order = 0
        self.round_time = 30

    def next_team(self,points):
        self.teams[self.order] += points
        self.order = (self.order + 1)% len(self.teams)
    
    def give_word(self):
        """
        Метод возвращает слово из словаря сессии

        :return: очередное слово
        """
        ret = self.dictionary[self.counter]
        self.counter += 1
        return ret
    
    def add_team(self,team : Team):
        """
        Метод добавляет в сессию новую команду

        :param team: класс Team, команда, которая будет добавлена в сессию, если её ещё там нет
        """
        if team not in self.teams:
            self.teams.append(team)
        else:
            print("попытка дважды добавить команд",team)
    
    def change_time(self, changed):
        """
        Метод изменяет время одного раунда в сессии

        :param changed: новое время
        """
        self.round_time = changed
    
    def clear(self):
        """
        Метод очищает все поля сессии
        """
        self.key = ''
        self.teams = []
        self.dictionary = []
        self.counter = 0

    def __repr__(self) -> str:
        return str(self.key)+ ' ' +str(self.counter)+ ' ' + str(self.round_time)+ ' ' +str(self.teams) 












