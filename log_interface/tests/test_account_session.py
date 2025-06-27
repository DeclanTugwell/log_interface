import unittest
import sqlite3
import os
from flask import Flask, g, jsonify, session, request
from werkzeug.security import generate_password_hash
from repositories.account_repository import AccountRepository, Account
from repositories.project_repository import ProjectRepository, Project
from repositories.project_user_repository import ProjectUserRepository, ProjectUser
from enums.account_type import AccountType
from enums.log_type import LogType
from routes.account_session import account_session_blueprint
import json


class TestAddSessionAuthentication(unittest.TestCase):
    """
    Integration tests for the add_session route, focusing on access control and broken authentication.
    """

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.secret_key = "test_secret"
        cls.app.config["TESTING"] = True
        cls.app.config['ENABLE_NOTIFICATIONS'] = False

        cls.db_conn = sqlite3.connect(":memory:")
        cls.db_conn.row_factory = sqlite3.Row

        def get_test_db():
            g.db = cls.db_conn
            return g.db

        AccountRepository.get_db = staticmethod(get_test_db)
        ProjectRepository.get_db = staticmethod(get_test_db)
        ProjectUserRepository.get_db = staticmethod(get_test_db)

        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        with cls.app.app_context():
            cls.db_conn.executescript(schema_sql)
            cls.db_conn.commit()

        cls.app.register_blueprint(account_session_blueprint)

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.db_conn.close()

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.account_repo = AccountRepository()
        self.project_repo = ProjectRepository()
        self.project_user_repo = ProjectUserRepository()

        self.admin_account = self.account_repo.add_item(Account(None, "admin", generate_password_hash("adminpass"), AccountType.Admin))
        self.standard_account = self.account_repo.add_item(Account(None, "user", generate_password_hash("userpass"), AccountType.Standard))
        self.project = self.project_repo.add_item(Project(None, self.standard_account.account_id, "Project 1"))
        self.standard_account_no_projects_associated = self.account_repo.add_item(Account(None, "unassociated_user", generate_password_hash("userpass"), AccountType.Standard))
        self.hardware_id = "hw-abc-123"
        self.log_list = [{
            "message": "Device booted",
            "logType": LogType.Information.value,
            "timestamp": ""
        }]

    def tearDown(self):
        with self.client.session_transaction() as sess:
            sess.clear()
        db = AccountRepository.get_db()
        db.execute("DELETE FROM log")
        db.execute("DELETE FROM user_session")
        db.execute("DELETE FROM project_user")
        db.execute("DELETE FROM project")
        db.execute("DELETE FROM account")
        db.commit()
        self.ctx.pop()

    def test__WHEN_admin_credentials_correct__THEN_session_created(self):
        payload = {
            "username": "admin",
            "password": "adminpass",
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list,
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test__WHEN_user_not_admin_and_not_associated__THEN_unauthorised(self):
        payload = {
            "username": "unassociated_user",
            "password": "userpass",
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["status"], "unauthorised")

    def test__WHEN_user_associated_with_project__THEN_session_created(self):
        self.project_user_repo.add_item(ProjectUser(self.standard_account.account_id, self.hardware_id, self.project.project_id))
        payload = {
            "username": "user",
            "password": "userpass",
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test__WHEN_password_incorrect__THEN_unauthorised(self):
        payload = {
            "username": "admin",
            "password": "wrongpass",
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 401)

    def test__WHEN_user_does_not_exist__THEN_unauthorised(self):
        payload = {
            "username": "ghost",
            "password": "doesnotexist",
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 401)

    def test__WHEN_payload_is_invalid_json__THEN_error_returned(self):
        response = self.client.post("/create_session", data="notjson", content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], "error")
        
    def test__WHEN_session_active__THEN_credentials_not_required(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.admin_account.account_id

        payload = {
            "projectId": self.project.project_id,
            "hardwareId": self.hardware_id,
            "logList": self.log_list
        }
        response = self.client.post("/create_session", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

