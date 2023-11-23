import json
from datetime import datetime
from account import AccountType, AccountManager
from transaction import TransactionManager

class FinancialReportGenerator:
    def __init__(self, account_manager = AccountManager(), transaction_manager = TransactionManager()):
        self.account_manager = account_manager
        self.transaction_manager = transaction_manager

    def generate_income_statement(self, start_date, end_date):
        """
        Generates an income statement for a specified period.
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        income = 0
        expenses = 0

        # Process each transaction to calculate income and expenses
        for transaction in self.transaction_manager.transactions:
            transaction_date = datetime.strptime(transaction.date, "%Y-%m-%d")
            if start_date <= transaction_date <= end_date:
                for account, amounts in transaction.postings:
                    if account.type == "Income":
                        income += amounts.get("USD", 0)  # Assuming USD for simplicity
                    elif account.type == "Expenses":
                        expenses += amounts.get("USD", 0)

        net_income = income - expenses
        return {
            "Income": income,
            "Expenses": expenses,
            "Net Income": net_income
        }

    def generate_balance_sheet(self, as_of_date):
        """
        Generates a balance sheet as of a specific date.
        """
        as_of_date = datetime.strptime(as_of_date, "%Y-%m-%d")

        assets = 0
        liabilities = 0
        equity = 0

        # Process accounts to calculate assets, liabilities, and equity
        for account_name, account in self.account_manager.accounts.items():
            account_balance = account.balances.get("USD", 0)  # Assuming USD for simplicity
            if account.type == "Asset":
                assets += account_balance
            elif account.type == "Liability":
                liabilities += account_balance
            elif account.type == "Equity":
                equity += account_balance

        return {
            "Assets": assets,
            "Liabilities": liabilities,
            "Equity": equity
        }

# Example usage (assuming account_manager and transaction_manager are already set up)
report_generator = FinancialReportGenerator()
income_statement = report_generator.generate_income_statement("2023-01-01", "2023-12-31")
balance_sheet = report_generator.generate_balance_sheet("2023-12-31")

print("Income Statement:", income_statement)
print("Balance Sheet:", balance_sheet)
