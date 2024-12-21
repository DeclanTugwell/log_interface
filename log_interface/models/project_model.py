from repositories.project_repository import *
from .log_model import LogModel

class ProjectModel(Project):
    """
    ProjectModel class - inherits from Project
    This class provides access to all the functionality relating to the project table.
    Encapsulates the ProjectRepository class, which is used to directly interact with the database table.
    Also, handles the associated logs via LogModel.
    """
    project_repository = ProjectRepository()
    log_list = []

    def __init__(self, project: Project):
        """
        Constructor for the ProjectModel class
        Takes a Project object and maps its attributes to the ProjectModel attributes
        """
        self.account_id = project.account_id
        self.project_id = project.project_id
        self.project_name = project.project_name

    @staticmethod
    def create_model_from_request(project_name, account_id):
        """
        Static method to create a new ProjectModel object from the provided project name and account id
        Returns a ProjectModel object based on the given data
        """
        return ProjectModel(Project(None, account_id, project_name))

    @staticmethod
    def fetch_project_by_id(id):
        """
        Static method to fetch a project by its project id (PK)
        Returns a ProjectModel object representing the project entry, or None if not found
        """
        project = ProjectRepository.get_item_by_project_id(id)
        if project is not None:
            project = ProjectModel(project)
        return project

    @staticmethod
    def fetch_projects():
        """
        Static method to fetch all projects
        Returns a list of ProjectModel objects, each representing a project
        Each project is populated with associated log entries
        """
        project_models = []
        for project in ProjectRepository.get_items():
            project_model = ProjectModel(project)
            project_model.populate()
            project_models.append(project_model)
        return project_models
    
    @staticmethod
    def fetch_projects_by_account_id(account_id):
        """
        Static method to fetch all projects associated with a specific account id
        Returns a list of ProjectModel objects, each representing a project
        Each project is populated with associated log entries
        """
        project_models = []
        for project in ProjectRepository.get_items_by_account_id(account_id):
            project_model = ProjectModel(project)
            project_model.populate()
            project_models.append(project_model)

        return project_models

    @staticmethod
    def fetch_project_by_project_name(project_name):
        """
        Static method to fetch a project by its project name (UK)
        Returns a Project object associated with the provided name
        """
        return ProjectRepository.get_item_by_project_name(project_name)

    def create_project(self):
        """
        Method to create a new project entry in the database using the project repository.
        Uses the current ProjectModel object's data to create the project
        """
        return self.project_repository.add_item(self)
    
    def delete_project(self):
        """
        Method to delete the project associated with this ProjectModel object from the database.
        """
        self.project_repository.delete_item(self)

    def populate(self):
        """
        Populates the current ProjectModel with associated logs from the LogModel.
        Retrieves and associates logs for the project by its project_id.
        """
        self.log_list = LogModel.fetch_logs_by_project_id(self.project_id)

    def delete_associated_logs(self):
        """
        Deletes all logs associated with the current project.
        Loops through the log list and calls delete_log() on each log.
        """
        for log in self.log_list:
            log.delete_log()