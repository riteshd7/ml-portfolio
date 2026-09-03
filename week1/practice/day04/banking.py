class BankAccount:
    """A simple bank account.

    Tracks balance and full transaction history. Withdrawals exceeding
    balance raise ValueError ("insufficient funds").
    """

    def __init__(self, owner: str, opening_balance: float = 0):
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self.balance = opening_balance
        self.history = []  # list of (kind, amount) tuples

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(("withdraw", amount))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"


class SavingsAccount(BankAccount):
    """Bank account that earns periodic interest."""

    def __init__(self, owner: str, opening_balance: float = 0, interest_rate: float = 0):
        super().__init__(owner, opening_balance)
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        interest_amount = self.balance * self.interest_rate
        self.balance += interest_amount
        self.history.append(("interest", interest_amount))

    def __repr__(self) -> str:
        return (
            f"SavingsAccount(owner={self.owner!r}, balance={self.balance}, "
            f"rate={self.interest_rate})"
        )


class Bank:
    """Manages multiple accounts. Accounts are identified by sequential
    ints starting at 1.

    A class that manages many accounts (composition, not inheritance —
    Bank HAS-A list of accounts, it doesn't IS-A account).
    """

    def __init__(self, name: str):  
        self.name = name
        self.accounts: dict[int, BankAccount] = {}  
        self.next_id = 1

    def open_account(self, owner: str, opening_balance: float = 0) -> int:
        account = BankAccount(owner, opening_balance)
        account_id = self.next_id
        self.accounts[account_id] = account
        self.next_id += 1
        return account_id
       
    def open_savings(self, owner: str, opening_balance: float = 0, interest_rate: float = 0) -> int:
        account = SavingsAccount(owner, opening_balance, interest_rate)
        account_id = self.next_id
        self.accounts[account_id] = account
        self.next_id += 1
        return account_id     

    def get(self, account_id: int) -> BankAccount:
        if account_id not in self.accounts:
            raise KeyError(f"no such account: {account_id}")      
        return self.accounts[account_id]   

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        # Look both accounts up first. If either is missing, this raises
        # KeyError immediately and nothing has been touched yet.
        from_account = self.get(from_id)
        to_account = self.get(to_id)

        # Check funds BEFORE mutating anything. If we withdrew first and
        # the deposit somehow failed, we'd have destroyed money. Checking
        # up front keeps the operation atomic: either both sides happen,
        # or neither does.
        if amount > from_account.balance:
            raise ValueError("insufficient funds")

        from_account.withdraw(amount)
        to_account.deposit(amount)

    @property
    def total_assets(self) -> float:
        return sum(account.balance for account in self.accounts.values())


if __name__ == "__main__":
    # BankAccount
    a = BankAccount("Alice", 100)
    a.deposit(50)
    assert a.balance == 150
    a.withdraw(30)
    assert a.balance == 120
    try:
        a.withdraw(1000)
    except ValueError:
        pass
    else:
        raise AssertionError("should have raised on overdraft")

    # SavingsAccount
    s = SavingsAccount("Bob", 1000, 0.05)
    s.apply_interest()
    assert s.balance == 1050
    s.deposit(50)  # inherited
    assert s.balance == 1100

    # Bank with transfer
    b = Bank("MyBank")
    a_id = b.open_account("Alice", 100)
    bo_id = b.open_account("Bob", 50)
    b.transfer(a_id, bo_id, 30)
    assert b.get(a_id).balance == 70
    assert b.get(bo_id).balance == 80
    assert b.total_assets == 150

    # transfer atomicity
    try:
        b.transfer(a_id, bo_id, 10000)
    except ValueError:
        pass
    assert b.get(a_id).balance == 70   # unchanged
    assert b.get(bo_id).balance == 80  # unchanged

    print("Banking tests passed.")
