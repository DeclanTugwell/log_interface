import unittest
from unittest.mock import patch, MagicMock
from models.project_model import ProjectModel
from repositories.project_repository import ProjectRepository
from models.log_model import LogModel
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

    @patch.object(LogModel, 'fetch_logs_by_project_id')
    def test__WHEN_populate_called__THEN_logs_populated_correctly(self, mock_fetch_logs_by_project_id):
        mock_fetch_logs_by_project_id.return_value = [
            MagicMock(log_id=1, project_id=1, log_type=LogType.Information, message="Log message 1", timestamp=datetime.now()),
            MagicMock(log_id=2, project_id=1, log_type=LogType.Bug, message="Log message 2", timestamp=datetime.now())
        ]
        
        project = MagicMock(project_id=1, account_id=1, project_name="Test Project")
        project_model = ProjectModel(project)
        
        project_model.populate()
        
        self.assertEqual(len(project_model.log_list), 2)
        mock_fetch_logs_by_project_id.assert_called_once_with(1)