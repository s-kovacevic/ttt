import unittest
from game.game import Board
from unittest.mock import MagicMock


class TestBoard(unittest.TestCase):

    def test_init(self):
        board = Board()
        self.assertEqual(board.state, [i for i in range(9)])

        custom_state = ['', 1, 2, 4, 6, 8, 11, 'b']
        board = Board(state=custom_state)
        self.assertEqual(board.state, custom_state)

    def test_is_over(self):
        board = Board()

        patched_available_positions = MagicMock(return_value=[1, 2])
        board.available_positions = patched_available_positions

        self.assertFalse(board.is_over())

        init_state = [i for i in range(9)]

        state = ['x', 'x', 'x'] + [''] * 6
        board.state = state
        self.assertTrue(board.is_over())

        state = [''] * 3 + ['x', 'x', 'x'] + [''] * 3
        board.state = state
        self.assertTrue(board.is_over())

        state = [''] * 6 + ['x', 'x', 'x']
        board.state = state
        self.assertTrue(board.is_over())

        state = init_state[:]
        state[0] = state[3] = state[6] = 'x'
        board.state = state
        self.assertTrue(board.is_over())

        state = init_state[:]
        state[1] = state[4] = state[7] = 'x'
        board.state = state
        self.assertTrue(board.is_over())

        state = init_state[:]
        state[2] = state[5] = state[8] = 'x'
        board.state = state
        self.assertTrue(board.is_over())

        state = init_state[:]
        state[0] = state[4] = state[8] = 'x'
        board.state = state
        self.assertTrue(board.is_over())

        state = init_state[:]
        state[0] = state[4] = state[8] = 'x'
        board.state = state
        self.assertTrue(board.is_over())

        board = Board()
        patched_available_positions = MagicMock(return_value=[])
        board.available_positions = patched_available_positions
        self.assertTrue(board.is_over())

    def test_available_positions(self):
        initial_state = [i for i in range(9)]
        board = Board()
        self.assertEqual(board.available_positions(), initial_state)

        new_state = initial_state[:]
        new_state[0] = 'x'
        board.state = new_state
        self.assertEqual(board.available_positions(), initial_state[1:])

    def test_winner(self):
        board = Board()
        self.assertIsNone(board.winner)

        board = Board()
        board.state = ['x'] * 9
        self.assertEqual(board.winner, 'x')

    def test_next_sign(self):
        board = Board()
        self.assertEqual(board.next_sign(), 'x')

        board.state[4] = 'x'
        self.assertEqual(board.next_sign(), 'o')
