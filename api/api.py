from flask import Blueprint, jsonify

api = Blueprint(name='api', import_name=__name__, url_prefix='/api')


@api.route('/ping')
def ping():
    """
    Used for connection check
    """
    return jsonify({'message': 'pong'})
