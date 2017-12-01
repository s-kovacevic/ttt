import time
import random


class Player(object):
    def __init__(self, sign):
        self.sign = sign

    def play(self, board):
        """
        This method should not print anything, just make the move since
        this will not be used when running from terminal
        :param board:
        :return:
        """
        raise NotImplementedError

    def play_cli(self, board):
        """
        This method will be called when Player should play the game ran from
        terminal
        :param board: board state list representation
        :return: None
        """
        raise NotImplementedError


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

    def play(self, board):
        pass


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

    def play(self, board):
        position = random.choice(board.available_positions())
        board.state[position] = self.sign


class UnbeatableBot(Player):

    def __init__(self, sign):
        super(UnbeatableBot, self).__init__(sign)

    def minimax(self, sign, board):
        """
        Recursive minimax algorithm. Basically, this algorithm will play every
        possible game till the end and calculate best-worst case scenario while
        taking in count that players switch turns.
        :param sign: sign of the next player either x or o
        :param board:
        :return: int 0 if this move will eventually lead to a tie in worst case
        scenario, 10 if this move leads to a victory, -10 if move leads to a
        loss
        """
        # TODO add weighting of returned integers so that shallower
        # solutions get better scores
        if board.is_over():
            if not board.winner:
                return 0
            if board.winner == self.sign:
                return 10
            if board.winner != self.sign:
                return -10

        position_values = {}

        # If current board has multiple solutions, recursively solve them and
        # store every position value
        for position in board.available_positions():
            copy_board = board.copy()
            copy_board.state[position] = sign
            position_values[position] = self.minimax(
                copy_board.next_sign(), copy_board
            )

        # Depending on which player is in charge, pick best or worst move
        # at that point
        if sign == self.sign:
            return max(position_values.values())
        else:
            return min(position_values.values())

    def play(self, board):
        available_positions = board.available_positions()

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
                copy_board.next_sign(), board=copy_board
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
