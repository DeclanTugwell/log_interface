import unittest
import sqlite3
import os
from flask import Flask, g
from repositories.account_repository import AccountRepository, Account
from enums.account_type import AccountType
from repositories.base_repository import BaseRepository


class TestAccountRepository(unittest.TestCase):
    """
    This test class integration tests methods related to the AccountRepository class.
    """

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True

        cls.db_conn = sqlite3.connect(':memory:')
        cls.db_conn.row_factory = sqlite3.Row

        def get_test_db():
            g.db = cls.db_conn
            return g.db

        AccountRepository.get_db = staticmethod(get_test_db)

        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        with cls.app.app_context():
            cls.db_conn.executescript(schema_sql)
            cls.db_conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db_conn.close()

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.repo = AccountRepository()

    def tearDown(self):
        self.repo.get_db().execute("DELETE FROM account")
        self.repo.get_db().commit()
        self.ctx.pop()

    def test__WHEN_add_item_called__WITH_valid_account__THEN_account_is_persisted(self):
        account = Account(None, "alice", "pass", AccountType.Standard)
        added = self.repo.add_item(account)

        self.assertEqual(added.username, "alice")

        accounts = AccountRepository.get_items()
        self.assertTrue(any(a.username == "alice" for a in accounts))

    def test__WHEN_get_item_by_id_called__WITH_existing_id__THEN_correct_account_returned(self):
        account = Account(None, "bob", "123", AccountType.Admin)
        added = self.repo.add_item(account)

        fetched = AccountRepository.get_item_by_id(added.account_id)

        self.assertEqual(fetched.username, "bob")
        self.assertEqual(fetched.account_type, AccountType.Admin)

    def test__WHEN_get_item_by_username_called__WITH_existing_username__THEN_account_is_returned(self):
        account = Account(None, "carol", "pw", AccountType.Standard)
        self.repo.add_item(account)

        fetched = AccountRepository.get_item_by_username("carol")

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.username, "carol")

    def test__WHEN_update_item_called__WITH_modified_account__THEN_changes_are_saved(self):
        account = Account(None, "dave", "pw", AccountType.Standard)
        added = self.repo.add_item(account)

        updated = Account(added.account_id, "dave", "pw", AccountType.Admin)
        self.repo.update_item(added.account_id, updated)

        fetched = AccountRepository.get_item_by_id(added.account_id)
        self.assertEqual(fetched.account_type, AccountType.Admin)

    def test__WHEN_delete_item_called__WITH_existing_account__THEN_account_is_removed(self):
        account = Account(None, "eve", "pw", AccountType.Standard)
        added = self.repo.add_item(account)

        self.repo.delete_item(added)

        fetched = AccountRepository.get_item_by_id(added.account_id)
        self.assertIsNone(fetched)

    def test__WHEN_malicious_username_inserted__THEN_sql_injection_is_prevented(self):
        malicious_input = "'; DROP TABLE account; --"
        account = Account(None, malicious_input, "pw", AccountType.Standard)
        added = self.repo.add_item(account)

        self.assertEqual(added.username, malicious_input)

        accounts = AccountRepository.get_items()
        self.assertIsInstance(accounts, list)

        db = BaseRepository.get_db()
        result = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='account'"
        ).fetchone()

        self.assertIsNotNone(result)