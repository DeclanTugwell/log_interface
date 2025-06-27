import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC
from models.log_model import LogModel
from repositories.log_repository import LogRepository
from enums.log_type import LogType

class TestLogModel(unittest.TestCase):
    """
    This test class unit tests methods related to the LogModel class that can be found in models.log_model
    """
    @patch.object(LogRepository, 'get_item_by_id')
    def test__WHEN_fetch_log_by_id_called__WITH_valid_log_id__THEN_correct_log_returned(self, mock_get_item_by_id):
        mock_get_item_by_id.return_value = MagicMock(log_id=1, project_id=1, log_type=LogType.Information, message="Log message", timestamp=datetime.now(UTC))
        
        log = LogModel.fetch_log_by_id(1)
        
        self.assertIsNotNone(log)
        self.assertEqual(log.log_id, 1)
        mock_get_item_by_id.assert_called_once_with(1)

    def test__WHEN_create_from_request_called__THEN_log_model_created_correctly(self):
        timestamp = datetime(2024, 12, 19, 15, 30)
        log_model = LogModel.create_from_request(1, "Log message", timestamp, LogType.Information)
        
        self.assertEqual(log_model.session_id, 1)
        self.assertEqual(log_model.message, "Log message")
        self.assertEqual(log_model.log_type, LogType.Information)
        self.assertEqual(log_model.timestamp, timestamp)

    @patch.object(LogRepository, 'add_item')
    def test__WHEN_create_log_called__THEN_log_added_to_repository(self, mock_add_item):
        timestamp = datetime(2024, 12, 19, 15, 30)
        log = MagicMock(log_id=None, project_id=1, log_type=LogType.Information, message="Log message", timestamp=timestamp)
        log_model = LogModel(log)
        
        log_model.create_log()
        
        mock_add_item.assert_called_once_with(log_model)

    @patch.object(LogRepository, 'delete_item')
    def test__WHEN_delete_log_called__THEN_log_deleted_from_repository(self, mock_delete_item):
        timestamp = datetime(2024, 12, 19, 15, 30)
        log = MagicMock(log_id=1, project_id=1, log_type=LogType.Information, message="Log message", timestamp=timestamp)
        log_model = LogModel(log)
        
        log_model.delete_log()
        
        mock_delete_item.assert_called_once_with(log_model)