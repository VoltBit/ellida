from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from settings import EllidaSettings

from .frontend import frontend
from .nav import nav

from colorama import init, Fore
init(autoreset=True)

import zmq

# context = zmq.Context()
# engine_socket = context.socket(zmq.PAIR)

# engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
#                        str(EllidaSettings.UI_SOCKET))


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    return app
