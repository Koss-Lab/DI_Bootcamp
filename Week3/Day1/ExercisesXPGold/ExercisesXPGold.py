#ExercisesXPGold.py

class BankAccount:
    def __init__(self, balance=0, username=None, password=None):
        self.balance = balance
        self.username = username
        self.password = password
        self.authenticated = False

    def authenticate(self, username, password):
        if self.username == username and self.password == password:
            self.authenticated = True
            print("✅ Authentication successful.")
        else:
            print("❌ Authentication failed.")

    def deposit(self, amount):
        if not self.authenticated:
            raise Exception("You must be authenticated to deposit.")
        if amount <= 0:
            raise Exception("Deposit must be a positive number.")
        self.balance += amount
        print(f"💰 Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if not self.authenticated:
            raise Exception("You must be authenticated to withdraw.")
        if amount <= 0:
            raise Exception("Withdrawal must be a positive number.")
        if amount > self.balance:
            raise Exception("Not enough balance.")
        self.balance -= amount
        print(f"💸 Withdrew {amount}. New balance: {self.balance}")


class MinimumBalanceAccount(BankAccount):
    def __init__(self, balance=0, minimum_balance=0, username=None, password=None):
        super().__init__(balance, username, password)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if not self.authenticated:
            raise Exception("You must be authenticated to withdraw.")
        if amount <= 0:
            raise Exception("Withdrawal must be a positive number.")
        if self.balance - amount < self.minimum_balance:
            raise Exception("Cannot withdraw: balance would go below minimum.")
        self.balance -= amount
        print(f"💸 Withdrew {amount}. New balance: {self.balance}")


class ATM:
    def __init__(self, account_list, try_limit):
        if not all(isinstance(acc, BankAccount) for acc in account_list):
            raise Exception("All accounts must be instances of BankAccount or its subclasses.")
        if not isinstance(try_limit, int) or try_limit <= 0:
            print("⚠️ Invalid try limit, defaulting to 2.")
            try_limit = 2

        self.account_list = account_list
        self.try_limit = try_limit
        self.current_tries = 0
        self.show_main_menu()

    def show_main_menu(self):
        while True:
            print("\n🏧 Main Menu:")
            print("1. Log in")
            print("2. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.log_in(username, password)
            elif choice == '2':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option.")

    def log_in(self, username, password):
        for account in self.account_list:
            account.authenticate(username, password)
            if account.authenticated:
                print(f"🎉 Welcome, {username}!")
                self.show_account_menu(account)
                return

        self.current_tries += 1
        if self.current_tries >= self.try_limit:
            print("🚫 Maximum login attempts reached. Shutting down...")
            exit()
        else:
            print(f"❌ Login failed. {self.try_limit - self.current_tries} attempts remaining.")

    def show_account_menu(self, account):
        while True:
            print("\n💳 Account Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                try:
                    amount = int(input("Enter deposit amount: "))
                    account.deposit(amount)
                except Exception as e:
                    print(f"⚠️ {e}")
            elif choice == '2':
                try:
                    amount = int(input("Enter withdrawal amount: "))
                    account.withdraw(amount)
                except Exception as e:
                    print(f"⚠️ {e}")
            elif choice == '3':
                print("🔒 Logging out...")
                account.authenticated = False
                break
            else:
                print("❌ Invalid option.")


# ---------------------------
# Example usage
# ---------------------------

if __name__ == "__main__":
    acc1 = BankAccount(500, "ariel", "1234")
    acc2 = MinimumBalanceAccount(300, 100, "nathan", "abcd")
    accounts = [acc1, acc2]

    ATM(accounts, 3)
