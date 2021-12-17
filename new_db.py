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
    def add_points(self, k : int):
        self.points += k
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
        self.round_time = 3
        self.temp_points = 0

    def next_team(self,points):
        self.temp_points += points
        print(self.temp_points)
        if self.teams[self.order].points + self.temp_points >= 5:
            self.teams[self.order].add_points(self.temp_points)
            #return 'Win'
            return 3
        elif self.counter % (self.round_time) == 0:
            self.teams[self.order].add_points(self.temp_points)
            self.order = (self.order + 1)% len(self.teams)
            self.temp_points = 0
            #return True
            return 1
        else:
            #return False
            return 2

    def cur_team(self):
        return self.teams[self.order].name

    def give_word(self):
        """
        Метод возвращает слово из словаря сессии

        :return: очередное слово
        """
        ret = self.dictionary[self.counter]
        self.counter += 1
        return ret
    
    def add_team(self,name):
        """
        Метод добавляет в сессию новую команду

        :param team: класс Team, команда, которая будет добавлена в сессию, если её ещё там нет
        """
        team = Team(name)
        if team not in self.teams:
            self.teams.append(team)
        else:
            print("попытка дважды добавить команду",team)
    
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












