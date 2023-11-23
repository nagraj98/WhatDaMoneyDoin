import json

from enum import Enum

class AccountType(Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EXPENSE = "Expense"
    INCOME = "Income"
    EQUITY = "Equity"


class Account:
    def __init__(self, account_type, name):

        if not account_type or not name:
            raise ValueError("Account type and name cannot be empty.")

        if not isinstance(account_type, AccountType):
            raise ValueError("account_type must be an instance of AccountType enum")
        
        self.type = account_type
        self.name = name
        self.balances = {}

    def add_balance(self, currency, amount):
        if not currency or amount is None:
            raise ValueError("Currency and amount cannot be empty.")

        if currency in self.balances:
            self.balances[currency] += amount
        else:
            self.balances[currency] = amount

    def edit_account(self, new_name=None, new_type=None):
        if new_name:
            self.name = new_name
        if new_type:
            self.type = new_type

    def to_dict(self):
        """
        Converts the Account instance into a dictionary for JSON serialization.
        """
        return {"type": self.type.value, "name": self.name, "balances": self.balances}

    @staticmethod
    def from_dict(data):
        """
        Creates an Account instance from a dictionary.
        """
        account = Account(AccountType(data["type"]), data["name"])
        account.balances = data.get("balances", {})
        return account

    def __str__(self):
        balances_str = ', '.join([f"{currency}: {amount}" for currency, amount in self.balances.items()])
        return f"Account Name: {self.name}, Type: {self.type}, Balances: {balances_str}"


class AccountManager:
    def __init__(self, data_file='accounts.json'):
        self.data_file = data_file
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """
        Loads accounts from a JSON file.
        """
        try:
            with open(self.data_file, 'r') as file:
                account_data = json.load(file)
                return {name: Account.from_dict(data) for name, data in account_data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_accounts(self):
        """
        Saves accounts to a JSON file.
        """
        with open(self.data_file, 'w') as file:
            account_dict = {name: account.to_dict() for name, account in self.accounts.items()}
            json.dump(account_dict, file, indent=4)

    def create_account(self, account_type, name):
        if name in self.accounts:
            raise ValueError("Account with this name already exists.")

        new_account = Account(account_type, name)
        self.accounts[name] = new_account
        self.save_accounts()

    def edit_account(self, name, new_name=None, new_type=None):
        if name not in self.accounts:
            raise ValueError("Account not found.")

        self.accounts[name].edit_account(new_name, new_type)
        if new_name:
            self.accounts[new_name] = self.accounts.pop(name)
        self.save_accounts()

    def update_account(self, name):
        """
        Updates the details of an existing account in the accounts dictionary.
        """
        if name not in self.accounts:
            raise ValueError("Account not found.")
        self.save_accounts()

    def get_account(self, name):
        return self.accounts.get(name)
    
    def get_all_accounts(self):
        """
        Returns a list of all available accounts.
        """
        return list(self.accounts.keys())





