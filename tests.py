import unittest
from new_db import Team, Session


class DbTest(unittest.TestCase):
    def setUp(self) -> None:
        self.team = Team(name='')
    def test_add_points(self): # test method names begin with 'test'
        a = self.team.points
        self.team.add_points(1)
        self.assertEqual(self.team.points, a + 1)
    if __name__ == '__main__':
        unittest.main()