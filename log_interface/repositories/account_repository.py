from .base_repository import BaseRepository
from enums.account_type import AccountType

class Account:
    """
    Account class - represents the schema for the account table in an object-oriented manner.
    This class encapsulates the attributes and structure of a user account.
    """
    account_id: int
    username: str
    password: str
    account_type: AccountType

    def __init__(self, account_id: int, username: str, password: str, account_type: AccountType):
        """
        Constructor for the Account class.
        Initializes an Account object with the provided account_id, username, password, and account_type.
        """
        self.account_id = account_id
        self.username = username
        self.password = password
        self.account_type = account_type

class AccountRepository(BaseRepository):
    """
    AccountRepository class - handles the interaction with the database for account-related operations.
    It provides methods to fetch, add, update, and delete account records in the database.
    """
    @staticmethod
    def get_items():
        """
        Static method to fetch all accounts from the account table.
        Returns a list of Account objects, each representing an account in the database.
        """
        account_list = []
        db = BaseRepository.get_db()
        items = db.execute("SELECT * FROM account").fetchall()
        for item in items:
            account_list.append(Account(item["account_id"], item["username"], item["password"], AccountType(item["account_type"])))
        return account_list
    
    @staticmethod
    def get_item_by_username(username):
        """
        Static method to fetch an account by its username (UK).
        Returns an Account object if found, otherwise returns None.
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM account WHERE username = ?", (username,)).fetchall()[0]
        except:
            item = None
        if item is not None:
            item = Account(item["account_id"], item["username"], item["password"], AccountType(item["account_type"]))
        return item

    @staticmethod
    def get_item_by_id(id):
        """
        Static method to fetch an account by its account id (PK).
        Returns an Account object if found, otherwise returns None.
        """
        db = BaseRepository.get_db()
        try:
            item = db.execute("SELECT * FROM account WHERE account_id = ?", (id,)).fetchall()[0]
        except:
            item = None
        if item is not None:
            item = Account(item["account_id"], item["username"], item["password"], AccountType(item["account_type"]))
        return item

    def add_item(self, item: Account):
        """
        Method to add a new account to the account table.
        Takes an Account object and inserts it into the database.
        Returns the newly created Account object with the generated account_id.
        """
        db = self.get_db()
        db.execute("INSERT INTO account (username, password, account_type) VALUES (?, ?, ?)", (item.username, item.password, item.account_type.value))
        db.commit()
        item = db.execute("SELECT * FROM account WHERE username = ? AND password = ? AND account_type = ?", (item.username, item.password, item.account_type.value)).fetchall()[0]
        return Account(item["account_id"], item["username"], item["password"], item["account_type"])

    def update_item(self, targetId, item: Account):
        """
        Method to update the account type of an existing account in the database.
        Takes the target account's id and the updated Account object.
        """
        db = self.get_db()
        db.execute("UPDATE account SET account_type = ? WHERE account_id = ?", (item.account_type.value, targetId))
        db.commit()

    def delete_item(self, item: Account):
        """
        Method to delete an account from the account table.
        Takes an Account object and removes it from the database by account_id.
        """
        db = self.get_db()
        db.execute("DELETE FROM account WHERE account_id = ?", (str(item.account_id),))
        db.commit()