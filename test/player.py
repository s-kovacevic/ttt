import unittest
from game.game import Board
from game.player import UnbeatableBot


class TestUnbeatableBot(unittest.TestCase):

    def test_minimax(self):
        """
        I can't possibly test all the possibilities so I present you this one
        case.
        """
        bot = UnbeatableBot('x')
        board = Board(state=['x', 'x', 'o', 'o', 'x', 'o', 'x', 'o', 8])
        score = bot.minimax('x', board=board)
        self.assertEqual(score, 19)
