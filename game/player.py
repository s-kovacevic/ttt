import time
import random
from abc import ABCMeta, abstractmethod
from game.exceptions import InvalidMoveError


class Player(metaclass=ABCMeta):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

    @abstractmethod
    def play(self, board, position=None):
        """
        This method should not print anything, just make the move since
        this will not be used when running from terminal
        :param board: instance of a Board class
        :param position: provide position if its a manual play(e.g.
        human player playing)
        """
        pass

    @abstractmethod
    def play_cli(self, board):
        """
        This method will be called when Player should play the game ran from
        terminal
        :param board: board state list representation
        :return: None
        """
        pass


class HumanPlayer(Player):
    """
    Used for human players
    """
    def __init__(self, sign):
        super(HumanPlayer, self).__init__(sign)

    def play_cli(self, board):
        prompt = '{} is playing (position 1-9): '.format(self.sign)
        position = int(input(prompt)) - 1
        while position not in board.available_positions():
            print('Nope, something is already there!')
            position = int(input()) - 1
        board.state[position] = self.sign

    def play(self, board, position=None):
        if position in board.available_positions():
            board.state[position] = self.sign
        else:
            raise InvalidMoveError()


class StupidBot(Player):
    """
    Stupid bot that just picks his next move at random from pool of
    available moves
    """
    def __init__(self, sign):
        super(StupidBot, self).__init__(sign)

    def play_cli(self, board):
        time.sleep(1)
        print('Stupid bot finished his turn...')
        self.play(board)

    def play(self, board, position=None):
        position = random.choice(board.available_positions())
        board.state[position] = self.sign


class UnbeatableBot(Player):

    def __init__(self, sign):
        super(UnbeatableBot, self).__init__(sign)

    def minimax(self, sign, board, depth=0):
        """
        Recursive minimax algorithm. Basically, this algorithm will play every
        possible game till the end and calculate best-worst case scenario while
        taking in count that players switch turns.
        :param sign: sign of the next player either x or o
        :param board: instance of the Board class
        :param depth: used to determine better move e.g. when multiple moves
        eventually result a victory, choose the quicker one and vice versa
        :return: int 0 if this move will eventually lead to a tie in worst case
        scenario, 10 + (10 - depth) if this move leads to a victory,
        -10 - (10 - depth) if move leads to a loss
        """
        if board.is_over():
            if not board.winner:
                return 0
            if board.winner == self.sign:
                # `10 - depth` because maximum depth can be 9 and the less deep
                # it is, the better
                return 10 + (10 - depth)
            else:
                # This won't matter much since he is not going to be losing
                # but if he is, he will make it as painful as possible.
                return -10 - (10 - depth)
        depth += 1

        position_values = {}

        # If current board has multiple solutions, recursively solve them and
        # store every position value
        for position in board.available_positions():
            copy_board = board.copy()
            copy_board.state[position] = sign
            position_values[position] = self.minimax(
                copy_board.next_sign, copy_board, depth
            )

        # Depending on which player is in charge, pick best or worst move
        # at that point
        if sign == self.sign:
            return max(position_values.values())
        else:
            return min(position_values.values())

    def play(self, board, position=None):
        available_positions = board.available_positions()

        if not available_positions:
            raise InvalidMoveError()

        # Optimizing so that if bot goes first it doesn't need to go
        # through 9 minimaxes to find out the obvious result.
        # It takes around 6 seconds to recursively solve all possible games on
        # my machine, and results will be 0 for each field, so lets skip that
        # and just play a corner
        if len(available_positions) == 9:
            board.state[random.choice([0, 2, 6, 8])] = self.sign
            return

        position_scores = {}
        for position in available_positions:
            # Call minimaxing for each available position and pick the one with
            # the highest score
            copy_board = board.copy()
            copy_board.state[position] = self.sign
            position_scores[position] = self.minimax(
                copy_board.next_sign, board=copy_board
            )
        best_position = max(
            position_scores.keys(),
            key=lambda key: position_scores[key]
        )
        board.state[best_position] = self.sign

    def play_cli(self, board):
        print('Thinking...')
        self.play(board)
        print('Unbeatable bot finished his turn...')
