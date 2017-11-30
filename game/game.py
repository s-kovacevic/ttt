class Board(object):
    def __init__(self, state=None):
        if not state:
            self.state = [i for i in range(9)]
        else:
            self.state = state

    def __str__(self):
        return (
            " {} | {} | {} \n"
            "-----------   \n"
            " {} | {} | {} \n"
            "-----------   \n"
            " {} | {} | {}   "
        ).format(*[i if not isinstance(i, int) else ' ' for i in self.state])

    def is_over(self):
        """
        :return: Boolean that shows whether or not game is over
        """
        if not self.available_positions():
            return True
        return (
            len({self.state[0], self.state[3], self.state[6]}) == 1 or
            len({self.state[1], self.state[4], self.state[7]}) == 1 or
            len({self.state[2], self.state[5], self.state[8]}) == 1 or
            len({self.state[0], self.state[1], self.state[2]}) == 1 or
            len({self.state[3], self.state[4], self.state[5]}) == 1 or
            len({self.state[6], self.state[7], self.state[8]}) == 1 or
            len({self.state[0], self.state[4], self.state[8]}) == 1 or
            len({self.state[2], self.state[4], self.state[6]}) == 1
        )

    def available_positions(self):
        """
        :return: List of positions that are still available for play
        """
        return [x for x in self.state if isinstance(x, int)]

    @property
    def winner(self):
        """
        :return: 'x', 'o' or None, depending on who won the game, None is for
        draw
        """
        if not self.available_positions():
            return None
        x_count = self.state.count('x')
        o_count = self.state.count('o')
        if x_count > o_count:
            return 'x'
        elif x_count == o_count:
            return 'o'


class Game(object):
    def __init__(self, board=None, players=None):
        if not board:
            self.board = Board()
        else:
            self.board = board
        if not players or len(players) < 2 < len(players):
            raise Exception('Need exactly 2 players!')
        self.players = players

    def play_cli(self):
        """
        Play the game of TicTacToe in terminal.
        """
        while not self.board.is_over():
            for player in self.players:
                print(str(self.board))
                player.play_cli(self.board)
                if self.board.is_over():
                    print(str(self.board))
                    print('Game is over, {}'.format(
                        'winner is: {}'.format(self.board.winner) if
                        self.board.winner else 'its a draw!'
                    ))
                    break
