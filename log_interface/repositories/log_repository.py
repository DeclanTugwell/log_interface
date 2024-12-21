from .base_repository import BaseRepository
from datetime import datetime
from enums.log_type import LogType

class Log:
    """
    Log class - represents the schema for a log entry in an object-oriented manner.
    Encapsulates the attributes and structure of a log entry, including project association and timestamp.
    """
    log_id: int
    project_id: int
    log_type: LogType
    message: str
    timestamp: datetime

    def __init__(self, log_id: int, project_id: int, log_type: LogType, message: str, timestamp: datetime):
        """
        Constructor for the Log class.
        Initializes a Log object with the provided log_id, project_id, log_type, message, and timestamp.
        """
        self.log_id = log_id
        self.project_id = project_id
        self.log_type = log_type
        self.message = message
        self.timestamp = timestamp

class LogRepository(BaseRepository):
    """
    LogRepository class - responsible for interacting with the database to manage log entries.
    Provides methods to fetch, add, update, and delete log entries in the database.
    """
    @staticmethod
    def get_items_by_project_id(id):
        """
        Static method to fetch all logs associated with a specific project id.
        Returns a list of Log objects, each representing a log entry related to the project.
        """
        log_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM log WHERE project_id = ?", (id,)).fetchall()
        for item in items:
            log_list.append(Log(item["log_id"], item["project_id"], LogType(int(item["log_type"])), item["message"], datetime.strptime(item["timestamp"], '%Y-%m-%d %H:%M:%S.%f'))) 
        return log_list
    
    @staticmethod
    def get_item_by_id(id):
        """
        Static method to fetch a specific log by its log id (PK).
        Returns a Log object representing the log entry, or None if the log does not exist.
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM log WHERE log_id = ?", (id,)).fetchall()[0]
            log = Log(item["log_id"], item["project_id"], LogType(int(item["log_type"])), item["message"], datetime.strptime(item["timestamp"], '%Y-%m-%d %H:%M:%S.%f'))
        except:
            log = None  
        return log
    
    def update_log_type(self, item: Log, log_type: LogType):
        """
        Method to update the log type of a specific log entry in the database.
        Takes a Log object and the new log type to update the record.
        """
        db = self.get_db()
        db.execute("UPDATE log SET log_type = ? WHERE log_id = ?", (log_type.value, item.log_id))
        db.commit()

    def add_item(self, item: Log):
        """
        Method to add a new log entry to the log table.
        Takes a Log object and inserts it into the database.
        """
        db = self.get_db()
        db.execute("INSERT INTO log (project_id, log_type, message, timestamp) VALUES (?, ?, ?, ?)", (item.project_id, item.log_type.value, item.message, item.timestamp))
        db.commit()

    def delete_item(self, item: Log):
        """
        Method to delete a specific log entry from the log table.
        Takes a Log object and removes it from the database by log_id.
        """
        db = self.get_db()
        db.execute("DELETE FROM log WHERE log_id = ?", (str(item.log_id),))
        db.commit()