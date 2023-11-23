import json
from account import AccountManager

class Transaction:
    def __init__(self, date, time, description, postings = []):
        self.date = date
        self.time = time
        self.description = description
        self.postings = postings

    def add_posting(self, account, amounts):
        """
        Adds a posting to the transaction.
        :param account: The account associated with the posting.
        :param amounts: Dictionary of amounts in various currencies.
        """
        self.postings.append((account, amounts))

    def is_valid(self):
        """
        Checks if the transaction is valid. A valid transaction has the sum of amounts in all postings equal to zero for each currency.
        """
        currency_totals = {}
        for _, amounts in self.postings:
            for currency, amount in amounts.items():
                currency_totals[currency] = currency_totals.get(currency, 0) + amount

        return all(total == 0 for total in currency_totals.values())

    def register_transaction(self):
        """
        Registers the transaction, applying its postings to the respective accounts.
        """
        if not self.is_valid():
            raise ValueError("Cannot register an invalid transaction.")

        for account, amounts in self.postings:
            for currency, amount in amounts.items():
                account.add_balance(currency, amount)

    def __str__(self):
        postings_str = '\n'.join([f"{account.name} {amounts}" for account, amounts in self.postings])
        return f"Date: {self.date}, Time: {self.time}, Description: {self.description}, Postings:\n{postings_str}"



class TransactionManager:
    def __init__(self, account_manager = AccountManager(), data_file='transactions.json', ):
        self.data_file = data_file
        self.account_manager = account_manager
        self.transactions = self.load_transactions()

    def load_transactions(self):
        """
        Loads transactions from a JSON file.
        """
        try:
            with open(self.data_file, 'r') as file:
                transaction_data = json.load(file)
                return [self._dict_to_transaction(data) for data in transaction_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transactions(self):
        """
        Saves transactions to a JSON file.
        """
        with open(self.data_file, 'w') as file:
            transaction_dicts = [self._transaction_to_dict(transaction) for transaction in self.transactions]
            json.dump(transaction_dicts, file, indent=4)

    def _transaction_to_dict(self, transaction):
        """
        Converts a Transaction instance to a dictionary for JSON serialization.
        """
        postings = [{"account": posting[0], "amounts": posting[1]} for posting in transaction.postings]
        return {
            "date": transaction.date,
            "time": transaction.time,
            "description": transaction.description,
            "postings": postings
        }

    def _dict_to_transaction(self, data):
        """
        Creates a Transaction instance from a dictionary.
        """
        postings = [(self.account_manager.get_account(posting["account"]), posting["amounts"]) for posting in data["postings"]]
        return Transaction(data["date"], data["time"], data["description"], postings)

    def add_transaction_old(self, date, time, description, postings):
        """
        Creates and adds a new transaction.
        """
        # Validation for the transaction parameters
        if not date or not time or not description:
            raise ValueError("Date, time, and description are required for a transaction.")
        if not postings:
            raise ValueError("At least one posting is required for a transaction.")

        new_transaction = Transaction(date, time, description, postings)
        if not new_transaction.is_valid():
            raise ValueError("Invalid transaction: postings do not balance to zero.")
        
        self.transactions.append(new_transaction)
        self.save_transactions()
    
    def add_transaction(self, date, time, description, postings):
        """
        Creates and adds a new transaction, and applies it to the involved accounts.
        """
        if not date or not time or not description:
            raise ValueError("Date, time, and description are required for a transaction.")
        if not postings:
            raise ValueError("At least one posting is required for a transaction.")

        new_transaction = Transaction(date, time, description, postings)
        if not new_transaction.is_valid():
            raise ValueError("Invalid transaction: postings do not balance to zero.")

        # Update account balances through AccountManager
        for account_name, amounts in postings:
            for currency, amount in amounts.items():
                # self.account_manager.update_account_balance(account.name, currency, amount)
                account = self.account_manager.get_account(account_name)
                account.add_balance(currency, amount)
                self.account_manager.update_account(account_name)

        self.transactions.append(new_transaction)
        self.save_transactions()
