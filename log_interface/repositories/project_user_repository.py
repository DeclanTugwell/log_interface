from .base_repository import BaseRepository

class ProjectUser:
    user_id: int
    hardware_id: str
    project_id: int

    def __init__(self, user_id: int, hardware_id : str, project_id: int):
        self.project_id = project_id
        self.hardware_id = hardware_id
        self.user_id = user_id

class ProjectUserRepository(BaseRepository):

    @staticmethod
    def get_items():
        """
        Static method to fetch all projects from the project table.
        This method returns a list of Project objects, each representing a project entry in the database.
        """
        project_user_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM project_user").fetchall()
        for item in items:
            project_user_list.append(ProjectUser(item["user_id"], item["hardware_id"], item["project_id"]))
        return project_user_list
    
    @staticmethod
    def get_item_by_project_id(id):
        """
        Static method to fetch specific project users by their project_id (FK).
        """
        project_user_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM project_user WHERE project_id = ?", (id,)).fetchall()
        for item in items:
            project_user_list.append(ProjectUser(item["user_id"], item["hardware_id"], item["project_id"]))
        return project_user_list
    
    @staticmethod
    def get_item_by_hardware_id(hardware_id):
        db = BaseRepository.get_db()
        try:
            returned_item = db.execute("SELECT * FROM project_user WHERE hardware_id = ?", (hardware_id,)).fetchall()[0]
            item = ProjectUser(int(returned_item["user_id"]), returned_item["hardware_id"], int(returned_item["project_id"]))
        except:
            item = None
        return item
    
    @staticmethod
    def get_item_by_project_user_id(project_user_id):
        db = BaseRepository.get_db()
        try:
            returned_item = db.execute("SELECT * FROM project_user WHERE user_id = ?", (project_user_id,)).fetchall()[0]
            item = ProjectUser(int(returned_item["user_id"]), returned_item["hardware_id"], int(returned_item["project_id"]))
        except:
            item = None
        return item
    
    def add_item(self, item: ProjectUser):
        db = self.get_db()
        db.execute("INSERT INTO project_user (hardware_id, project_id) VALUES (?, ?)", (item.hardware_id, item.project_id,))
        db.commit()
        return self.get_item_by_hardware_id(item.hardware_id)

    def delete_item(self, item: ProjectUser):
        """
        Method to delete a specific project entry from the project table.
        This method takes a Project object and removes it from the database using the project's project_id.
        """
        db = self.get_db()
        db.execute("DELETE FROM project_user WHERE hardware_id = ?", (str(item.hardware_id),))
        db.commit()