from flask import Blueprint, jsonify, request
from game import (
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


@api.route('/<uuid:game_id>/status', methods=['GET'])
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
