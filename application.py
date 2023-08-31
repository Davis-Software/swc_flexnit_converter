import os

from flask import Flask
from flask_socketio import SocketIO
from tools.cache import Cache
from tools.config import Config

from engineio.async_drivers import threading

cache = Cache()

working_dir = os.path.dirname(os.path.realpath(__file__))
config = Config(os.path.join(working_dir, 'config.ini'))

app = Flask(__name__)
socketio = SocketIO(app, asnc_mode="threading")

app.secret_key = config.get("SECRET_KEY")


with app.app_context():
    from routes import http, socket
