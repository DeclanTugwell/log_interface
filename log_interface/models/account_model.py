from enums.account_type import AccountType
from repositories.account_repository import *
from .project_model import ProjectModel
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
)

class AccountModel(Account):
    """
    AccountModel class - inherits from Account
    This class provides access to all the functionality relating to the account table.
    Encapsulated the AccountRepository class which is used to directly interact with the database table.
    """
    account_repository = AccountRepository()

    def __init__(self, account: Account):
        """
        Constructor class, takes an Account object
        """
        self.account_id = account.account_id
        self.username = account.username
        self.password = account.password
        self.account_type = account.account_type

    @staticmethod
    def fetch_account_by_username(username):
        """
        Static method used to fetch an account by the account username (UK), when received it populates and returns an AccountModel object with it.
        """
        account = AccountRepository.get_item_by_username(username)
        if account is not None:
            account = AccountModel(account)
        return account
    
    @staticmethod
    def fetch_account_by_id(id):
        """
        Static method used to fetch an account by the account id (PK), when received it populates and returns an AccountModel object with it.
        """
        account = AccountRepository.get_item_by_id(id)
        if account is not None:
            account = AccountModel(account)
        return account

    @staticmethod
    def fetch_accounts():
        """
        Static method used to fetch all accounts within the account table, returned as a list of Account objects.
        """
        return AccountRepository.get_items()
    
    @staticmethod
    def from_registration(username, password, is_admin):
        """
        Static method used to construct and return an AccountModel based on the data received during registration.
        """
        hashed_password = generate_password_hash(password)
        if (is_admin == True):
            account_type = AccountType.Admin
        else:
            account_type = AccountType.Standard
        return AccountModel(Account(None, username, hashed_password, account_type))
    
    @staticmethod
    def validate_username_password_entry(username, password):
        """
        Static method used to validate the username and password entered during registration, returns a list of errors during validation. The list is empty of the credentials are valid
        """
        error_messages = policy.test(password)
        if " " in username:
            error_messages.append("Username cannot contain a space")
        return error_messages
    
    def fetch_associated_populated_projects(self):
        is_admin = self.is_admin()
        if (is_admin):
            projects = ProjectModel.fetch_projects()
        else:
            projects = ProjectModel.fetch_projects_by_account_id(self.account_id)
        return projects
    
    def create_account(self):
        """
        Create account method, this will take the properties of the AccountModel and create a record within the account table
        """
        return self.account_repository.add_item(self)
    
    def is_admin(self):
        """
        Returns whether the current account is an admin
        """
        is_admin = False
        if (self.account_type == AccountType.Admin):
            is_admin = True
        return is_admin
    
    def is_associated_with_project(self, project_id):
        is_associated = False
        associated_projects = ProjectModel.fetch_projects_by_account_id(self.account_id)
        for project in associated_projects:
            if project.project_id == project_id:
                is_associated = True

        return is_associated
    
    def delete_account(self):
        """
        Removed the account associated with this object from the account table
        """
        self.account_repository.delete_item(self)