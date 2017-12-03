from game import Game
from util import limited_input
from game.player import HumanPlayer, StupidBot, UnbeatableBot


if __name__ == '__main__':
    # Maybe add the option to watch 2 unbeatable bots play tie games, somebody
    # would probably find that amusing
    against = limited_input(
        prompt='Play versus:\n1 - friend\n2 - stupid bot\n3 - unbeatable bot\n',
        limit_to=['1', '2', '3'],
        help_='1, 2 or 3 please.'
    )

    sign = limited_input(
        prompt='Pick your sign (x or o):',
        limit_to=['x', 'o'],
        help_='x or o please.'
    )

    Bot = StupidBot if against == '2' else UnbeatableBot
    if against == '1':
        players = [HumanPlayer('x'), HumanPlayer('o')]
    else:
        players = [HumanPlayer(sign), Bot('x' if sign == 'o' else 'o')]

    game = Game(players=players)
    game.play_cli()
