import os
from flask import Flask
from repositories.base_repository import BaseRepository
from flask_socketio import SocketIO

socket = SocketIO()

def init_db(app):
    """
    Initialises the database
    """
    try:
        with app.app_context():
            db = BaseRepository.get_db()
            with app.open_resource("schema.sql", mode="r") as f:
                db.executescript(f.read())
                db.commit()
    except:
        print("Database already initialised.")

# Defines the application configuration
def initialise_app():
    app = Flask(__name__)
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, "/data", os.getenv('DATABASE', 'data.db')),
        SECRET_KEY=os.urandom(24),
    ))
    socket.init_app(app)
    return app