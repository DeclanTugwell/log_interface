from repositories.log_repository import *

class LogModel(Log):
    """
    LogModel class - inherits from Log
    This class provides access to all the functionality relating to the log table.
    Encapsulates the LogRepository class, which is used to directly interact with the database table.
    """
    log_repository = LogRepository()
    format_string = "%Y-%m-%d %H:%M:%S"

    def __init__(self, log: Log):
        """
        Constructor for the LogModel class
        Takes a Log object and maps its attributes to the LogModel attributes.
        """
        self.log_id = log.log_id
        self.project_id = log.project_id
        self.log_type = log.log_type
        self.message = log.message
        self.timestamp = log.timestamp
        self.timestamp_str = log.timestamp.strftime(self.format_string)
    
    @staticmethod
    def fetch_logs_by_project_id(project_id):
        """
        Static method used to fetch all logs for a given project id.
        Returns a list of LogModel objects, each representing a log entry
        """
        log_models = []
        for log in LogRepository.get_items_by_project_id(project_id):
            log_model = LogModel(log)
            log_models.append(log_model)

        return log_models
    
    @staticmethod
    def fetch_log_by_id(log_id):
        """
        Static method used to fetch a specific log by its log id (PK).
        Returns a LogModel object representing the log entry
        """
        return LogModel(LogRepository.get_item_by_id(log_id))
    
    @staticmethod
    def create_from_request(project_id: int, message: str, timestamp: datetime, log_type: LogType):
        """
        Static method to create a new LogModel from the provided request data
        Returns a new LogModel object based on the provided parameters
        """
        return LogModel(Log(None, project_id, log_type, message, timestamp))

    def create_log(self):
        """
        Method to create a new log entry in the database using the log repository
        Uses the current LogModel object's data to create the log
        """
        return self.log_repository.add_item(self)
    
    def delete_log(self):
        """
        Method to delete the log associated with this LogModel object from the database
        """
        self.log_repository.delete_item(self)

    def update_type(self, log_type: LogType):
        """
        Method to update the log type of this log entry in the database
        """
        self.log_repository.update_log_type(self, log_type)

    def serialise(self):
        """
        Method to convert the LogModel object into a dictionary format that can be serialised into JSON.
        This allows the log data to be easily transmitted or stored in JSON format
        """
        return {
            "log_id": self.log_id,
            "project_id": self.project_id,
            "log_type": self.log_type.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }