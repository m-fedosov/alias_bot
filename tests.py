import unittest
from new_db import Team, Session


class TeamTest(unittest.TestCase):
    def setUp(self) -> None:
        self.team = Team(name='')
    def test_add_points1(self): # test method names begin with 'test'
        a = self.team.points
        self.team.add_points(1)
        self.assertEqual(self.team.points, a + 1)
    def test_add_points3(self): # test method names begin with 'test'
        a = self.team.points
        self.team.add_points(3)
        self.assertEqual(self.team.points, a + 3)
    def test_repr0(self):
        a = Team('test')
        self.assertEqual(str(a), 'test 0')
    def test_repr15(self):
        a = Team('test')
        for i in range(3):
            a.add_points(5)
        self.assertEqual(str(a), 'test 15')
    if __name__ == '__main__':
        unittest.main()