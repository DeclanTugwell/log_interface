import unittest
from unittest.mock import patch, MagicMock
from models.project_model import ProjectModel
from models.user_session_model import UserSession
from models.project_user_model import ProjectUser
from repositories.project_repository import ProjectRepository
from repositories.project_user_repository import ProjectUserRepository
from repositories.user_session_repository import UserSessionRepository
from repositories.log_repository import LogRepository
from models.log_model import Log
from enums.log_type import LogType
from datetime import datetime

class TestProjectModel(unittest.TestCase):
    """
    This test class unit tests methods related to the ProjectModel class that can be found in models.project_model
    """

    @patch.object(ProjectRepository, 'get_item_by_project_id')
    def test__WHEN_fetch_project_by_id_called__WITH_valid_project_id__THEN_correct_project_returned(self, mock_get_item_by_project_id):
        mock_get_item_by_project_id.return_value = MagicMock(project_id=1, account_id=1, project_name="Test Project")
        
        project = ProjectModel.fetch_project_by_id(1)
        
        self.assertIsNotNone(project)
        self.assertEqual(project.project_id, 1)
        mock_get_item_by_project_id.assert_called_once_with(1)

    def test__WHEN_create_model_from_request_called__THEN_project_model_created_correctly(self):
        project_model = ProjectModel.create_model_from_request("Test Project", 1)
        
        self.assertEqual(project_model.project_name, "Test Project")
        self.assertEqual(project_model.account_id, 1)

    @patch.object(ProjectRepository, 'add_item')
    def test__WHEN_create_project_called__THEN_project_added_to_repository(self, mock_add_item):
        project = MagicMock(project_id=None, account_id=1, project_name="Test Project")
        project_model = ProjectModel(project)
        
        project_model.create_project()
        
        mock_add_item.assert_called_once_with(project_model)

    @patch.object(ProjectRepository, 'delete_item')
    def test__WHEN_delete_project_called__THEN_project_deleted_from_repository(self, mock_delete_item):
        project = MagicMock(project_id=1, account_id=1, project_name="Test Project")
        project_model = ProjectModel(project)
        
        project_model.delete_project()
        
        mock_delete_item.assert_called_once_with(project_model)