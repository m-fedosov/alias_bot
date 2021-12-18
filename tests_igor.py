import select
import unittest

from new_db import Team, Session
from randomize_dict import randomize_dict
from session_key_generator import gen_session_key
class SessionTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.session = Session(key = '')
    
    def test_change_max_score_15(self):
        self.session.change_max_score(15)
        self.assertEqual(self.session.max_score, 15)
    
    def test_change_max_score_0(self):
        self.session.change_max_score(0)
        self.assertEqual(self.session.max_score, 0)
    
    def test_cur_team_no(self):
        self.session.add_team('test')
        self.assertEqual(self.session.cur_team(), self.session.teams[self.session.order].name)
    
    def test_cur_team_2teams(self):
        self.session.add_team('test')
        self.session.add_team('test1')
        self.session.order = 1
        self.assertEqual(self.session.cur_team(), self.session.teams[self.session.order].name)
    
    def test_give_word_first_then_second(self):
        first = self.session.dictionary[0]
        self.assertEqual(self.session.counter, 0)
        self.assertEqual(self.session.give_word(), first)
        second = self.session.dictionary[1]
        self.assertEqual(self.session.counter, 1)
        self.assertEqual(self.session.give_word(), second)

    def test_give_word_nth(self):
        for i in range(len(self.session.dictionary)):
            self.session.counter = i
            self.assertEqual(self.session.give_word(), self.session.dictionary[i])

    def test_add_team_not_empty(self):
        team1 = Team('test1')
        self.session.add_team(team1)
        self.assertNotEqual(len(self.session.teams), 0)

    def test_add_team_length2(self):
        team1 = Team('test1')
        team2 = Team('test2')
        self.session.add_team(team1)
        self.session.add_team(team2)
        self.assertEqual(len(self.session.teams), 2)

    def test_add_team_length1000(self):
        for i in range(1000):
            self.session.add_team(f'test{i}')
        self.assertEqual(len(self.session.teams), 1000)
    
    def test_add_team_already_in_teams(self):
        self.session.add_team('test')
        self.assertEqual(self.session.add_team('test'), 0)

    def test_change_time_not_default_3(self):
        a = self.session.round_time
        self.session.change_time(0)
        self.assertNotEqual(self.session.round_time, a)
    
    def test_change_time_10(self):
        self.session.change_time(10)
        self.assertEqual(self.session.round_time, 10)
    
    def test_changes_and_clear_all(self):
        for i in range(3):
            self.session.add_team(f'test{i}')
        for team in self.session.teams:
            team.points = 5
        for team in self.session.teams:
            self.assertEqual(team.points, 5)
        self.session.counter = 5
        self.assertEqual(self.session.counter, 5)
        self.session.temp_points = 6
        self.assertEqual(self.session.temp_points, 6)
        self.session.clear()
        for team in self.session.teams:
            self.assertEqual(team.points, 0)
        self.assertEqual(self.session.counter, 0)
        self.assertEqual(self.session.temp_points, 0)
        
    def test_randomize_diff(self):
        self.session.dictionary = randomize_dict()
        b = randomize_dict()
        self.assertNotEqual(self.session.dictionary, b)
    def test_key_gen_1000(self): #тыща разов если вдруг что
        for i in range(1000):
            self.assertNotEqual(gen_session_key(),gen_session_key())
    def test_repr(self):
        self.session.counter = 3
        self.assertIn(str(self.session.counter),str(self.session))
    def test_get_info(self):
        self.session.teams = [Team('1'),Team('2')]
        self.assertIn("'1', '2'", self.session.get_info())

    if __name__ == '__main__':
        unittest.main()