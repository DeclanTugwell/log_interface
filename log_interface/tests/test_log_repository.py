import unittest
import sqlite3
import os
from flask import Flask, g
from datetime import datetime, UTC
from repositories.log_repository import LogRepository, Log
from enums.log_type import LogType


class TestLogRepository(unittest.TestCase):
    """
    This test class integration tests methods related to the LogRepository class.
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

        LogRepository.get_db = staticmethod(get_test_db)

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
        self.repo = LogRepository()

    def tearDown(self):
        self.repo.get_db().execute("DELETE FROM log")
        self.repo.get_db().commit()
        self.ctx.pop()

    def test__WHEN_add_item_called__WITH_valid_log__THEN_log_is_persisted(self):
        log = Log(None, 1, LogType.Information, "Initial log message", datetime.now(UTC))
        self.repo.add_item(log)

        logs = LogRepository.get_items_by_session_id(1)
        self.assertTrue(any(l.message == "Initial log message" for l in logs))

    def test__WHEN_get_items_by_session_id_called__WITH_existing_session_id__THEN_logs_are_returned(self):
        timestamp = datetime.now(UTC)
        log1 = Log(None, 100, LogType.Bug, "Bug found", timestamp)
        log2 = Log(None, 100, LogType.Event, "Session started", timestamp)
        self.repo.add_item(log1)
        self.repo.add_item(log2)

        logs = LogRepository.get_items_by_session_id(100)

        self.assertEqual(len(logs), 2)
        self.assertTrue(all(log.session_id == 100 for log in logs))

    def test__WHEN_get_item_by_id_called__WITH_existing_id__THEN_correct_log_is_returned(self):
        timestamp = datetime.now(UTC)
        log = Log(None, 200, LogType.Warning, "This is a warning", timestamp)
        self.repo.add_item(log)

        log_id = self.repo.get_db().execute("SELECT log_id FROM log WHERE session_id = ?", (200,)).fetchone()["log_id"]
        fetched = LogRepository.get_item_by_id(log_id)

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.message, "This is a warning")
        self.assertEqual(fetched.log_type, LogType.Warning)

    def test__WHEN_update_log_type_called__WITH_new_type__THEN_log_type_is_updated(self):
        log = Log(None, 300, LogType.Event, "Generic event", datetime.now(UTC))
        self.repo.add_item(log)

        log_id = self.repo.get_db().execute("SELECT log_id FROM log WHERE session_id = ?", (300,)).fetchone()["log_id"]
        stored_log = LogRepository.get_item_by_id(log_id)
        self.repo.update_log_type(stored_log, LogType.Bug)

        updated_log = LogRepository.get_item_by_id(log_id)
        self.assertEqual(updated_log.log_type, LogType.Bug)

    def test__WHEN_delete_item_called__WITH_existing_log__THEN_log_is_removed(self):
        log = Log(None, 400, LogType.Information, "To be removed", datetime.now(UTC))
        self.repo.add_item(log)

        log_id = self.repo.get_db().execute("SELECT log_id FROM log WHERE session_id = ?", (400,)).fetchone()["log_id"]
        stored_log = LogRepository.get_item_by_id(log_id)
        self.repo.delete_item(stored_log)

        deleted_log = LogRepository.get_item_by_id(log_id)
        self.assertIsNone(deleted_log)

    def test__WHEN_malicious_log_message_inserted__THEN_sql_injection_is_prevented(self):
        log = Log(None, 1, LogType.Information, "'; DROP TABLE log;--", datetime.now())
        self.repo.add_item(log)

        logs = LogRepository.get_items_by_session_id(1)
        self.assertTrue(any("'; DROP TABLE log;--" in log.message for log in logs))