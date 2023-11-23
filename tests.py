import unittest
import os
from account import AccountManager, AccountType
from transaction import TransactionManager
from datetime import datetime

class FinanceAppTests(unittest.TestCase):

    def setUp(self):
        # Define test data files
        self.test_account_data_file = 'test_accounts.json'
        self.test_transaction_data_file = 'test_transactions.json'

        # Ensure test data files are clean before each test
        self.cleanup_files()

        # Set up AccountManager and TransactionManager for testing
        self.account_manager = AccountManager(data_file=self.test_account_data_file)
        self.transaction_manager = TransactionManager(data_file=self.test_transaction_data_file, account_manager=self.account_manager)

    def tearDown(self):
        # Clean up test data files after each test
        self.cleanup_files()

    def cleanup_files(self):
        # Delete test data files if they exist
        for file in [self.test_account_data_file, self.test_transaction_data_file]:
            if os.path.exists(file):
                os.remove(file)

    # Tests for AccountManager
    def test_account_creation_and_retrieval(self):
        self.account_manager.create_account(AccountType.INCOME, "Salary Account")
        account = self.account_manager.get_account("Salary Account")
        self.assertIsNotNone(account)
        self.assertEqual(account.type, AccountType.INCOME)

    # ... More tests for AccountManager ...

    # Tests for TransactionManager
    def test_transaction_creation_and_application(self):
        # Create test accounts
        self.account_manager.create_account(AccountType.INCOME, "Salary")
        self.account_manager.create_account(AccountType.EXPENSE, "Rent")

        account = self.account_manager.get_account("Salary")
        self.assertIsNotNone(account)

        account = self.account_manager.get_account("Rent")
        self.assertIsNotNone(account)

        # Create and add a transaction
        postings = [("Salary", {"USD": 1000}), ("Rent", {"USD": -1000})]
        self.transaction_manager.add_transaction(datetime.today().strftime('%Y-%m-%d'), "10:00:00", "Salary Payment", postings)
        
        # Test if the transaction was added and applied correctly
        salary_account = self.account_manager.get_account("Salary")
        rent_account = self.account_manager.get_account("Rent")
        self.assertEqual(salary_account.balances.get("USD", 0), 1000)
        self.assertEqual(rent_account.balances.get("USD", 0), -1000)

    # ... More tests for TransactionManager ...

if __name__ == '__main__':
    unittest.main()
