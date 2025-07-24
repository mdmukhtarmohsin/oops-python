class Account:
    bank_name = "Default Bank"
    minimum_balance = 0
    _total_accounts = 0

    def __init__(self, account_number, holder_name, balance):
        if not holder_name or balance < 0:
            raise ValueError("Invalid account details")
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        Account._total_accounts += 1

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < Account.minimum_balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self):
        return self.balance

    @classmethod
    def get_total_accounts(cls):
        return cls._total_accounts

    @classmethod
    def set_bank_name(cls, name):
        cls.bank_name = name

    @classmethod
    def set_minimum_balance(cls, amount):
        cls.minimum_balance = amount

    def __str__(self):
        return f"{self.account_number} - {self.holder_name} (${self.balance})"


class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, balance, interest_rate):
        super().__init__(account_number, holder_name, balance)
        if interest_rate < 0:
            raise ValueError("Interest rate must be non-negative")
        self.interest_rate = interest_rate

    def calculate_monthly_interest(self):
        return self.balance * (self.interest_rate / 100) / 12

    def __str__(self):
        return f"SavingsAccount({super().__str__()}, Interest: {self.interest_rate}%)"


class CheckingAccount(Account):
    def __init__(self, account_number, holder_name, balance, overdraft_limit):
        super().__init__(account_number, holder_name, balance)
        if overdraft_limit < 0:
            raise ValueError("Overdraft limit must be non-negative")
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < -self.overdraft_limit:
            return False
        self.balance -= amount
        return True

    def __str__(self):
        return f"CheckingAccount({super().__str__()}, Overdraft: ${self.overdraft_limit})"


savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)

print(f"Savings Account: {savings_account}")
print(f"Checking Account: {checking_account}")

print(f"Savings balance before: ${savings_account.get_balance()}")
savings_account.deposit(500)
print(f"After depositing $500: ${savings_account.get_balance()}")

withdrawal_result = savings_account.withdraw(200)
print(f"Withdrawal result: {withdrawal_result}")
print(f"Balance after withdrawal: ${savings_account.get_balance()}")

print(f"Checking balance: ${checking_account.get_balance()}")
overdraft_result = checking_account.withdraw(600)  
print(f"Overdraft withdrawal: {overdraft_result}")
print(f"Balance after overdraft: ${checking_account.get_balance()}")

interest_earned = savings_account.calculate_monthly_interest()
print(f"Monthly interest earned: ${interest_earned}")

print(f"Total accounts created: {Account.get_total_accounts()}")
print(f"Bank name: {Account.bank_name}")

Account.set_bank_name("New National Bank")
Account.set_minimum_balance(100)

try:
    invalid_account = SavingsAccount("SA002", "", -100, 1.5)
except ValueError as e:
    print(f"Validation error: {e}")
