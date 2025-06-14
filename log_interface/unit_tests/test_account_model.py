import unittest
from unittest.mock import patch, MagicMock
from models.account_model import AccountModel
from repositories.account_repository import AccountRepository, Account
from enums.account_type import AccountType
from repositories.base_repository import BaseRepository

class TestAccountModel(unittest.TestCase):
    """
    This test class unit tests methods related to the AccountModel class that can be found in models.account_model
    """
    @patch.object(AccountRepository, 'get_item_by_username')
    def test__WHEN_account_by_username_called__WITH_correct_name__THEN_correct_account_returned(self, mock_get_item_by_username):
        mock_get_item_by_username.return_value = MagicMock(account_id=1, username="testuser", password="password123", account_type=AccountType.Standard)
        
        account = AccountModel.fetch_account_by_username("testuser")
        
        self.assertIsNotNone(account)
        self.assertEqual(account.username, "testuser")
        mock_get_item_by_username.assert_called_once_with("testuser")

    @patch.object(AccountRepository, 'get_item_by_id')
    def test__WHEN_fetch_account_by_id_called__WITH_correct_id__THEN_correct_account_returned(self, mock_get_item_by_id):
        mock_get_item_by_id.return_value = MagicMock(account_id=1, username="testuser", password="password123", account_type=AccountType.Standard)
        
        account = AccountModel.fetch_account_by_id(1)
        
        self.assertIsNotNone(account)
        self.assertEqual(account.account_id, 1)
        mock_get_item_by_id.assert_called_once_with(1)

    @patch.object(AccountRepository, 'get_items')
    def test__WHEN_fetch_accounts_called__THEN_all_account_returned(self, mock_get_items):
        mock_get_items.return_value = [
            MagicMock(account_id=1, username="user1", password="pass1", account_type=AccountType.Standard),
            MagicMock(account_id=2, username="user2", password="pass2", account_type=AccountType.Admin)
        ]
        
        accounts = AccountModel.fetch_accounts()
        
        self.assertEqual(len(accounts), 2)
        mock_get_items.assert_called_once()

    def test__WHEN_from_registration_called__THEN_account_correctly_populated(self):
        account = AccountModel.from_registration("testuser", "password123", is_admin=False)
        
        self.assertEqual(account.username, "testuser")
        self.assertEqual(account.account_type, AccountType.Standard)

    def test__WHEN_validate_username_password_entry_called__WITH_valid_input__THEN_true_returned(self):
        result = AccountModel.validate_username_password_entry("validuser", "securepass123")
        
        self.assertTrue(len(result) == 0)

    def test__WHEN_validate_username_password_entry_called__WITH_valid_input__THEN_true_returned(self):
        self.assertTrue(len(AccountModel.validate_username_password_entry("bad user", "short")) > 0)
        self.assertTrue(len(AccountModel.validate_username_password_entry("gooduser", "short")) > 0)
        self.assertTrue(len(AccountModel.validate_username_password_entry("gooduser", None)) > 0)

    def test__WHEN_is_admin_called__THEN_appropriate_value_returned(self):
        account = Account(1, "testuser", "password123", AccountType.Standard)
        standard_account = AccountModel(account)

        account = Account(1, "testuser", "password123", AccountType.Admin)
        admin_account = AccountModel(account)

        self.assertFalse(standard_account.is_admin())
        self.assertTrue(admin_account.is_admin())