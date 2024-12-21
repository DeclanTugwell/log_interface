import os
from flask import Flask
from repositories.base_repository import *
from models.account_model import *
from routes import register_endpoints

def init_db():
    """
    Initialises the database
    """
    with app.app_context():
        db = BaseRepository.get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.executescript(f.read())
            db.commit()

# Defines the application configuration
app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, os.getenv('DATABASE', 'database.db')),
    SECRET_KEY=os.urandom(24),
))

# Registers endpoints used within the application
register_endpoints(app)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)