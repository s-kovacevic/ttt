from game.game import Game
from game.player import HumanPlayer, StupidBot


if __name__ == '__main__':
    print('Play versus:')
    print('1 - friend')
    print('2 - stupid bot')

    against = input()
    while against not in ['1', '2']:
        print('1 or 2 please.')
        against = input()

    sign = input('Pick your sign (x or o):')
    while sign not in ['x', 'o']:
        print('x or o please.')
        sign = input()

    if against == '1':
        players = [HumanPlayer('x'), HumanPlayer('o')]
    else:
        if sign == 'x':
            players = [HumanPlayer('x'), StupidBot('o')]
        else:
            players = [StupidBot('x'), HumanPlayer('o')]

    game = Game(players=players)
    game.play_cli()
