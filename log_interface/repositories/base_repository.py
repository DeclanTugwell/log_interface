import sqlite3
from flask import g

class BaseRepository():
    """
    Base Repository class - inherited by all other repositories.
    Provides functionality to fetch the database being used by the application
    """
    @staticmethod
    def get_db():
        """
        Fetches the database being used by the application
        """
        if "db" not in g:
            g.db = sqlite3.connect("data.db")
            g.db.row_factory = sqlite3.Row

        return g.db