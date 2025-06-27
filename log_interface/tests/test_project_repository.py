import unittest
import sqlite3
import os
from flask import Flask, g
from repositories.project_repository import Project, ProjectRepository

class TestProjectRepository(unittest.TestCase):
    """
    Unit tests for ProjectRepository class
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

        ProjectRepository.get_db = staticmethod(get_test_db)

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
        self.repo = ProjectRepository()

    def tearDown(self):
        self.repo.get_db().execute("DELETE FROM project")
        self.repo.get_db().commit()
        self.ctx.pop()

    def test__WHEN_add_item_called__THEN_project_inserted_and_returned(self):
        project = Project(None, 1, "Test Project")
        added = self.repo.add_item(project)
        self.assertIsNotNone(added.project_id)
        self.assertEqual(added.project_name, "Test Project")

    def test__WHEN_get_items_called__THEN_all_projects_returned(self):
        self.repo.add_item(Project(None, 1, "Project A"))
        self.repo.add_item(Project(None, 1, "Project B"))
        projects = ProjectRepository.get_items()
        self.assertEqual(len(projects), 2)

    def test__WHEN_get_item_by_project_id_called__WITH_valid_id__THEN_correct_project_returned(self):
        added = self.repo.add_item(Project(None, 1, "Unique Project"))
        fetched = ProjectRepository.get_item_by_project_id(added.project_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.project_name, "Unique Project")

    def test__WHEN_get_item_by_project_name_called__WITH_valid_name__THEN_correct_project_returned(self):
        self.repo.add_item(Project(None, 2, "Named Project"))
        fetched = ProjectRepository.get_item_by_project_name("Named Project")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.project_name, "Named Project")

    def test__WHEN_get_items_by_account_id_called__WITH_valid_id__THEN_only_matching_projects_returned(self):
        self.repo.add_item(Project(None, 3, "Account 3 Project A"))
        self.repo.add_item(Project(None, 3, "Account 3 Project B"))
        self.repo.add_item(Project(None, 4, "Account 4 Project"))
        projects = ProjectRepository.get_items_by_account_id(3)
        self.assertEqual(len(projects), 2)
        self.assertTrue(all(p.account_id == 3 for p in projects))

    def test__WHEN_delete_item_called__THEN_project_removed_from_db(self):
        added = self.repo.add_item(Project(None, 5, "To Be Deleted"))
        self.repo.delete_item(added)
        fetched = ProjectRepository.get_item_by_project_id(added.project_id)
        self.assertIsNone(fetched)

    def test__WHEN_malicious_project_name_inserted__THEN_sql_injection_is_prevented(self):
        project = Project(None, 1, "NormalProject")
        self.repo.add_item(project)

        malicious_name = "'; DROP TABLE project;--"
        
        result = ProjectRepository.get_item_by_project_name(malicious_name)
        self.assertIsNone(result)

        normal_project = ProjectRepository.get_item_by_project_name("NormalProject")
        self.assertIsNotNone(normal_project)