from .base_repository import BaseRepository

class Project:
    """
    Project class - represents the schema for the project table in an object-oriented manner.
    This class encapsulates the attributes and structure of a project, including the project ID,
    the associated account ID, and the project name.
    """
    project_id: int
    account_id: int
    project_name: str

    def __init__(self, project_id: int, account_id: int, project_name: str):
        """
        Constructor for the Project class.
        Initializes a Project object with the provided project_id, account_id, and project_name.
        """
        self.project_id = project_id
        self.project_name = project_name
        self.account_id = account_id

class ProjectRepository(BaseRepository):
    """
    ProjectRepository class - responsible for interacting with the database to manage project entries.
    Provides methods to fetch, add, update, and delete project entries in the database.
    """

    @staticmethod
    def get_items():
        """
        Static method to fetch all projects from the project table.
        This method returns a list of Project objects, each representing a project entry in the database.
        """
        project_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM project").fetchall()
        for item in items:
            project_list.append(Project(item["project_id"], item["account_id"], item["project_name"]))
        return project_list
    
    @staticmethod
    def get_item_by_project_id(id):
        """
        Static method to fetch a specific project by its project_id (PK).
        This method returns a Project object representing the project entry if found, or None if the project does not exist.
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM project WHERE project_id = ?", (id,)).fetchall()[0]
        except:
            item = None
        if (item is not None):
            item = Project(item["project_id"], item["account_id"], item["project_name"])
        return item
    
    @staticmethod
    def get_item_by_project_name(project_name):
        """
        Static method to fetch a specific project by its project_name.
        This method returns a Project object representing the project entry if found, or None if the project does not exist.
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM project WHERE project_name = ?", (project_name,)).fetchall()[0]
        except:
            item = None
        if (item is not None):
            item = Project(item["project_id"], item["account_id"], item["project_name"])
        return item
    
    @staticmethod
    def get_items_by_account_id(id):
        """
        Static method to fetch all projects associated with a specific account_id.
        This method returns a list of Project objects, each representing a project entry related to the account.
        """
        project_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM project WHERE account_id = ?", (id,)).fetchall()
        for item in items:
            project_list.append(Project(item["project_id"], item["account_id"], item["project_name"]))
        return project_list

    def add_item(self, item: Project):
        """
        Method to add a new project entry to the project table.
        This method takes a Project object and inserts it into the database.
        After insertion, it returns the Project object with its assigned project_id.
        """
        db = self.get_db()
        db.execute("INSERT INTO project (account_id, project_name) VALUES (?, ?)", (item.account_id, item.project_name))
        db.commit()
        item = db.execute("SELECT * FROM project WHERE account_id = ? AND project_name = ?", (item.account_id, item.project_name)).fetchall()[0]
        return Project(item["project_id"], item["account_id"], item["project_name"])

    def delete_item(self, item: Project):
        """
        Method to delete a specific project entry from the project table.
        This method takes a Project object and removes it from the database using the project's project_id.
        """
        db = self.get_db()
        db.execute("DELETE FROM project WHERE project_id = ?", (str(item.project_id),))
        db.commit()