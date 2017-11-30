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
