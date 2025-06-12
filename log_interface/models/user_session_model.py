from repositories.user_session_repository import *
from .log_model import LogModel
from datetime import datetime, timezone, timedelta
from enums.log_type import LogType
from services.database_notification_service import send_notification

class UserSessionModel(UserSession):
    user_session_repository = UserSessionRepository()
    timestamp_str = ""
    log_list = []
    warning_count = 0
    error_count = 0
    info_count = 0
    event_count = 0

    def __init__(self, session_user: UserSession):
        self.session_id = session_user.session_id
        self.user_id = session_user.user_id

    @staticmethod
    def create_model_from_request(user_id):
        return UserSessionModel(UserSession(None, user_id))

    @staticmethod
    def fetch_user_sessions():
        user_session_models = []
        for user_session in UserSessionRepository.get_items():
            user_session_model = UserSessionModel(user_session)
            user_session_model.populate()
            user_session_models.append(user_session_model)
        return user_session_models
    
    @staticmethod
    def fetch_user_session_by_user_id(user_id):
        user_session_models = []
        for user_session in UserSessionRepository.get_items_by_user_id(user_id):
            user_session_model = UserSessionModel(user_session)
            user_session_model.populate()
            user_session_models.append(user_session_model)

        return user_session_models
    
    @staticmethod
    def fetch_user_session_by_session_id(session_id):
        user_session = UserSessionRepository.get_item_by_session_id(session_id)
        if user_session is not None:
            user_session = UserSessionModel(user_session)
            user_session.populate()
            
        return user_session

    def create_user_session(self):
        sessionModel = UserSessionModel(self.user_session_repository.add_item(self))
        return sessionModel
    
    
    def delete_user_session(self):
        self.user_session_repository.delete_item(self)
        self.delete_associated_logs()

    def populate(self):
        """
        Populates the current ProjectModel with associated logs from the LogModel.
        Retrieves and associates logs for the project by its project_id.
        """
        self.log_list = LogModel.fetch_logs_by_session_id(self.session_id)
        earliest_timestamp = datetime(3000, 1, 1, tzinfo=timezone(timedelta(hours=0)))
        self.__reset_log_type_count()
        for log in self.log_list:
            if log.timestamp < earliest_timestamp:
                earliest_timestamp = log.timestamp
            self.__update_log_type_count(log)
        self.timestamp_str = earliest_timestamp.isoformat()

    def delete_associated_logs(self):
        """
        Deletes all logs associated with the current project.
        Loops through the log list and calls delete_log() on each log.
        """
        for log in self.log_list:
            log.delete_log()

    def __reset_log_type_count(self):
        self.error_count = 0
        self.event_count = 0
        self.warning_count = 0
        self.info_count = 0

    def __update_log_type_count(self, log: LogModel):
        if log.log_type == LogType.Bug:
            self.error_count = self.error_count + 1
        elif log.log_type == LogType.Information:
            self.info_count = self.info_count + 1
        elif log.log_type == LogType.Warning:
            self.warning_count = self.warning_count + 1
        elif log.log_type == LogType.Event:
            self.event_count = self.event_count + 1
    
    def serialise(self):
        return {
            "session_id": self.session_id,
            "timestamp_str": self.timestamp_str,
            "log_list": [log.serialise() for log in self.log_list],
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "info_count": self.info_count,
            "event_count": self.event_count
        }
