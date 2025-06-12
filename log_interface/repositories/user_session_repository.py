from .base_repository import BaseRepository

class UserSession:
    session_id: int
    user_id: int

    def __init__(self, session_id: int, user_id: int):
        self.session_id = session_id
        self.user_id = user_id

class UserSessionRepository(BaseRepository):

    @staticmethod
    def get_items():
        user_session_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM user_session").fetchall()
        for item in items:
            user_session_list.append(UserSession(item["session_id"], item["user_id"]))
        return user_session_list
    
    @staticmethod
    def get_items_by_user_id(id):
        """
        Static method to fetch specific project users by their user_id (FK).
        """
        user_session_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM user_session WHERE user_id = ?", (id,)).fetchall()
        for item in items:
            user_session_list.append(UserSession(int(item["session_id"]), int(item["user_id"])))
        return user_session_list
    
    @staticmethod
    def get_item_by_session_id(id):
        """
        Static method to fetch specific project users by their user_id (FK).
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM user_session WHERE session_id = ?", (id,)).fetchall()[0]
            item = UserSession(int(item["session_id"]), int(item["user_id"]))
        except:
            item = None
        return item
    
    def add_item(self, item: UserSession):
        db = self.get_db()
        db.execute("INSERT INTO user_session (user_id) VALUES (?)", (item.user_id,))
        db.commit()
        try:
            return self.get_items_by_user_id(item.user_id)[-1]
        except:
            return None

    def delete_item(self, item: UserSession):
        db = self.get_db()
        db.execute("DELETE FROM user_session WHERE session_id = ?", (str(item.session_id),))
        db.commit()