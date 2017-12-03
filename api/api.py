from flask import Blueprint, jsonify, request
from game import (
    player,
    Game,
    InvalidMoveError
)

# TODO This code needs input validation with cerberus and proper error handling
# Nobody got time fot that

api = Blueprint(name='api', import_name=__name__, url_prefix='/api')


@api.route('/ping')
def ping():
    """
    Used for connection check
    """
    return jsonify({'message': 'pong'})


@api.route('/game/new', methods=['POST'])
def new_game():
    """
    Endpoint that initiates a new game.
    Request should look like:
    {
        "x": "HumanPlayer",
        "o": "UnbeatableBot"
    }
    Possible types of players are: HumanPlayer, UnbeatableBot and StupidBot
    :return: id of the newly created game
    {
        "game_id": UUID
    }
    """
    data = request.get_json(force=True)
    if 'x' not in data or 'o' not in data:
        return jsonify({'error': 'Invalid request, missing field(s).'}), 400

    # Again this hacky thing...
    x_player = getattr(player, data['x'], None)(sign='x')
    o_player = getattr(player, data['o'], None)(sign='o')

    if x_player is None or o_player is None:
        return jsonify({'error': 'Invalid request, wrong player type(s).'}), 400
    game = Game(players=[x_player, o_player])
    game.persist()
    return jsonify({
        'game_id': str(game.id_)
    })


@api.route('/game/<uuid:game_id>/status', methods=['GET'])
def status(game_id):
    """
    Returns general information about the game.
    :param game_id: UUID of the game
    """
    game = Game.load_from_database(str(game_id))

    if not game:
        return jsonify({'error': "Couldn't find the game with that ID"}), 404

    return jsonify(game.to_database_object())


@api.route('/game/<uuid:game_id>/play', methods=['POST'])
def play(game_id):
    """
    Expected body is:
    {
        "sign": "x",
        "position": 3  # 0-8, can be omitted if it's a Bot player's turn
    }
    :param game_id: UUID of the game
    """
    data = request.get_json(force=True)
    if 'sign' not in data or 'position' not in data:
        return jsonify({'error': 'Invalid request, missing field(s).'}), 400

    game = Game.load_from_database(str(game_id))
    if not game:
        return jsonify({'error': "Couldn't find the game with that ID"}), 404

    if game.board.next_sign == data['sign'] and not game.board.is_over():
        player = game.player_map[data['sign']]

        try:
            player.play(board=game.board, position=data['position'])
        except InvalidMoveError:
            return jsonify({'error': 'Invalid move.'}), 400
        game.persist()
        return '', 204

    # Just casually pass this back if it passes everything, no time for this
    return '', 400
