import logging
from flask import Flask
from util import setup_logger, get_config

setup_logger()
logger = logging.getLogger(__name__)

app = Flask(__name__)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        dest='debug',
        help='Run app in debug mode.'
    )
    cmd_args = parser.parse_args()

    app_config = get_config(section='WEBAPP')
    port = app_config['port']
    app.run(
        host=app_config['host'] or 'localhost',
        port=int(port) if port else 5000,
        debug=cmd_args.debug
    )
