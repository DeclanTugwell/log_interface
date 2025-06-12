from repositories.project_user_repository import *
from .user_session_model import UserSessionModel

class ProjectUserModel(ProjectUser):
    project_user_repository = ProjectUserRepository()
    session_list = []
    warning_count = 0
    error_count = 0
    info_count = 0
    event_count = 0

    def __init__(self, project_user: ProjectUser):
        self.user_id = project_user.user_id
        self.hardware_id = project_user.hardware_id
        self.project_id = project_user.project_id

    @staticmethod
    def create_model_from_request(hardware_id, project_id):
        return ProjectUserModel(ProjectUser(None, hardware_id, project_id))

    @staticmethod
    def fetch_projects():
        project_user_models = []
        for project_user in ProjectUserRepository.get_items():
            project_user_model = ProjectUserModel(project_user)
            project_user_model.populate()
            project_user_models.append(project_user_model)
        return project_user_models
    
    @staticmethod
    def fetch_project_users_by_project_id(project_id):
        project_user_models = []
        for project_user in ProjectUserRepository.get_item_by_project_id(project_id):
            project_user_model = ProjectUserModel(project_user)
            project_user_model.populate()
            project_user_models.append(project_user_model)

        return project_user_models
    
    @staticmethod
    def fetch_project_user_by_hardware_id(hardware_id):
        project_user = ProjectUserRepository.get_item_by_hardware_id(hardware_id)
        if project_user is not None:
            return ProjectUserModel(project_user)
        return project_user
    
    @staticmethod
    def fetch_project_user_by_project_user_id(project_user_id):
        project_user = ProjectUserRepository.get_item_by_project_user_id(project_user_id)
        if project_user is not None:
            return ProjectUserModel(project_user)
        return project_user

    def create_project_user(self):
        return self.project_user_repository.add_item(self)
    
    def delete_project_user(self):
        self.project_user_repository.delete_item(self)
        self.delete_associated_sessions()

    def populate(self):
        """
        Populates the current ProjectModel with associated logs from the LogModel.
        Retrieves and associates logs for the project by its project_id.
        """
        self.session_list = UserSessionModel.fetch_user_session_by_user_id(self.user_id)
        self.__reset_log_type_count()
        for session in self.session_list:
            session.populate()
            self.__update_log_type_count(session)

    def delete_associated_sessions(self):
        """
        Deletes all logs associated with the current project.
        Loops through the log list and calls delete_log() on each log.
        """
        for user_session in self.session_list:
            user_session.delete_user_session()

    def __reset_log_type_count(self):
        self.error_count = 0
        self.event_count = 0
        self.warning_count = 0
        self.info_count = 0

    def __update_log_type_count(self, session):
        self.error_count = self.error_count + session.error_count
        self.event_count = self.event_count + session.event_count
        self.warning_count = self.warning_count + session.warning_count
        self.info_count = self.info_count + session.info_count

    def serialise(self):
        return {
            "user_id": self.user_id,
            "hardware_id": self.hardware_id,
            "session_list": [session.serialise() for session in self.session_list],
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "info_count": self.info_count,
            "event_count": self.event_count
        }