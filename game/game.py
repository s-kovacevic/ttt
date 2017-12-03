import uuid
from game import player
from database import DatabaseMixin


class Board(object):

    def __init__(self, state=None):
        super().__init__()

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

    @property
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


class Game(DatabaseMixin):
    __table__ = 'games'

    def __init__(self, board=None, players=None, id_=None):
        """
        :param board: Instance of Board class if you have game that is already
        started
        :param players: List of 2 players that play this game, again, instances
        of Player class
        :param id_: UUID object
        """
        super().__init__()

        if not id_:
            id_ = uuid.uuid4()
        self.id_ = id_

        if not board:
            self.board = Board()
        else:
            self.board = board
        if not players or len(players) < 2 or len(players) > 2:
            raise Exception('Need exactly 2 players!')
        self.player_map = {p.sign: p for p in players}
        self.players = players

    def play_cli(self):
        """
        Play the game of TicTacToe in terminal.
        """
        while not self.board.is_over():
            current_player = self.player_map[self.board.next_sign]
            print(str(self.board))
            current_player.play_cli(self.board)
            if self.board.is_over():
                print(str(self.board))
                print('Game is over, {}'.format(
                    'winner is: {}'.format(self.board.winner) if
                    self.board.winner else 'its a draw!'
                ))
                break

    def to_database_object(self):
        """
        Implementation of DatabaseMixin to_database_object method
        :return: this objects nosql database representation (dict)
        """
        return {
            'id_': str(self.id_),
            'winner': self.board.winner,
            'next_sign': self.board.next_sign,
            'is_over': self.board.is_over(),
            'board': {
                'state': self.board.state
            },
            'players': [
                {
                    'sign': p.sign,
                    'type': p.__class__.__name__
                } for p in self.players
            ],
        }

    @staticmethod
    def from_database_object(db_object):
        """
        Static method that builds python game object from database dictionary
        :param db_object: object that database return for the
        :return: Game instance that was created from db_object
        """
        board = Board(state=db_object['board']['state'])
        db_players = db_object['players']

        # This is so hacky that is gives me anxiety but it's fun...
        # Im getting the class from players module by it's name and
        # and instantiating it with the params. And of course, no time for
        # error handling.
        players = [
            getattr(player, p['type'])(sign=p['sign']) for p in db_players
        ]
        return Game(
            board=board, players=players, id_=uuid.UUID(db_object['id_'])
        )
