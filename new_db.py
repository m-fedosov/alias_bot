from randomize_dict import randomize_dict


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

    def add_points(self, k: int):
        """
        Метод добавляет k очков команде

        :param k: количество очков, которые нужно добавить
        """
        self.points += k

    def __repr__(self) -> str:
        return str(self.name) + ' ' + str(self.points)


class Session:
    """
    Класс сессии, хранит информацию о сессии

    """

    def __init__(self, key):
        """
        Конструктор\n
        Атрибут counter - указатель на слово для выдачи\n
        Атрибут order - номер команды отвечающей в данный момент\n
        Атрибут teams - хранит список команд, добавленных в данную сессию (элементы класса Team)\n
        Атрибут round_time - хранит значение, указывющее на количестов слов выдаваемых  в одном раунде\n
        Атрибут temp_points - временная переменная для хранения очков, потом очки передаются соответствующей комндае,
        переманная обнуляется\n
        Атрибут max_score - количесвто очков, которе необходимо набрать для победы одной из команд\n

        :param key: ключ сессии
        """
        self.teams = []

        self.dictionary = randomize_dict()  # перемешанный словарь
        self.key = key  # ключ сессии
        self.counter = 0  # указатель на слово для выдачи
        self.order = 0  # номер команды отвечающей в данный момент
        self.round_time = 3
        self.temp_points = 0
        self.max_score = 10

    def next_team(self, points):
        """
        Метод логики игры\n
        
        Возвращает одно из трех значений - 1, 2 или 3.\n
        Если функция возвращает 1, то ход переходит к другой команде\n
        Если 2, раунд продолжается\n
        Если 3, игра заканчивается\n
        Принимает на вход количество очков, на которое необходимо увеличить счет команды - 0 или 1\n
        :param points: количество очков, на которое увеличивается количество очков команды,
        когда она успешно объясняет слово (тогда он равен 1) или пропускает его (тогда равен 0)\n
        """
        self.temp_points += points
        
        if self.teams[self.order].points + self.temp_points >= self.max_score:
            self.teams[self.order].add_points(self.temp_points)
            return 3
        elif self.counter % (self.round_time) == 0:
            self.teams[self.order].add_points(self.temp_points)
            self.order = (self.order + 1) % len(self.teams)
            self.temp_points = 0
            return 1
        else:
            return 2

    def change_max_score(self, new_max):
        """
        метод изменяет количество очков необходимых для победы одной из команд
        :param new_max: новое значение
        """
        self.max_score = new_max

    def cur_team(self):
        """
        Метод возвращает название команды, которая в данный момент отвечает
        """
        return self.teams[self.order].name

    def give_word(self):
        """
        Метод возвращает слово из словаря сессии

        :return: очередное слово
        """
        ret = self.dictionary[self.counter]
        self.counter += 1
        return ret

    def add_team(self, name):
        """
        Метод добавляет в сессию новую команду

        :param team: класс Team, команда, которая будет добавлена в сессию, если её ещё там нет
        """
        team = Team(name)
        for i in self.teams:
            if i.name == team.name:
                return 0
        self.teams.append(team)

    def change_time(self, changed):
        """
        Метод изменяет время одного раунда в сессии

        :param changed: новое время
        """
        self.round_time = changed

    def clear(self):
        """
        Метод очищает поля сессии
        """
        for team in self.teams:
            team.points = 0
        self.counter = 0
        self.temp_points = 0

    def get_info(self) -> str:
        """
        Метод возвращает строку, содержащую информацию о параметрах, данной сессии
        """
        return f'Команды в текущей игре: {str([i.name for i in self.teams])}\nДлительность раунда: {str(self.round_time)}\nЧтобы выиграть, надо набрать {str(self.max_score)}'

    def __repr__(self) -> str:
        return str(self.key) + ' ' + str(self.counter) + ' ' + str(self.round_time) + ' ' + str(self.teams)


x = Session('asd')

