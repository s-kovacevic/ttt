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

    def copy(self):
        """
        :return: copy of the current board but with the new state list
        attached to it
        """
        return Board(state=self.state[:])

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

    def next_sign(self):
        """
        :return: sign of the next player
        """
        if self.state.count('o') == self.state.count('x'):
            return 'x'
        return 'o'

    @property
    def winner(self):
        """
        :return: 'x', 'o' or None, depending on who won the game, None is for
        draw
        """
        winning_positions = (
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 4, 8),
            (2, 4, 6),
        )
        for wp in winning_positions:
            characters = {
                self.state[wp[0]], self.state[wp[1]], self.state[wp[2]]
            }
            if len(characters) == 1:
                return characters.pop()


class Game(object):
    def __init__(self, board=None, players=None):
        if not board:
            self.board = Board()
        else:
            self.board = board
        if not players or len(players) < 2 or len(players) > 2:
            raise Exception('Need exactly 2 players!')
        self.players = players

    def play_cli(self):
        """
        Play the game of TicTacToe in terminal.
        """
        player_map = {p.sign: p for p in self.players}
        while not self.board.is_over():
            player = player_map[self.board.next_sign()]
            print(str(self.board))
            player.play_cli(self.board)
            if self.board.is_over():
                print(str(self.board))
                print('Game is over, {}'.format(
                    'winner is: {}'.format(self.board.winner) if
                    self.board.winner else 'its a draw!'
                ))
                break
