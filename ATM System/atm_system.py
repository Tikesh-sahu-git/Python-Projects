import sqlite3
import random
import time


class Account:
    def __init__(self, account_number, pin, name, balance):
        self.account_number = account_number
        self.pin = pin
        self.name = name
        self.balance = balance

    @staticmethod
    def create_table():
        with sqlite3.connect("atm.db") as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                pin TEXT NOT NULL,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )''')

    def save(self):
        with sqlite3.connect("atm.db") as conn:
            conn.execute(
                "INSERT INTO accounts (account_number, pin, name, balance) VALUES (?, ?, ?, ?)",
                (self.account_number, self.pin, self.name, self.balance)
            )

    def update_balance(self, new_balance):
        with sqlite3.connect("atm.db") as conn:
            conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                         (new_balance, self.account_number))
        self.balance = new_balance  # Update the instance variable after successful DB update

    def log_transaction(self, detail):
        with sqlite3.connect("atm.db") as conn:
            conn.execute("INSERT INTO transactions (account_number, details) VALUES (?, ?)", 
                         (self.account_number, detail))

    def change_pin(self, new_pin):
        with sqlite3.connect("atm.db") as conn:
            conn.execute("UPDATE accounts SET pin = ? WHERE account_number = ?", 
                        (new_pin, self.account_number))
        self.pin = new_pin  # Update the instance variable after successful DB update
        self.log_transaction("PIN changed")

    @staticmethod
    def get(account_number):
        with sqlite3.connect("atm.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
            row = cur.fetchone()
            return Account(*row) if row else None

    @staticmethod
    def get_transactions(account_number):
        with sqlite3.connect("atm.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT details, timestamp FROM transactions WHERE account_number = ? ORDER BY timestamp DESC", 
                       (account_number,))
            return cur.fetchall()


class ATM:
    def __init__(self):
        Account.create_table()
        self.current_account = None

    def generate_account_number(self):
        random.seed(time.time())
        return ''.join(str(random.randint(0, 9)) for _ in range(10))

    def create_account(self):
        print("\nCreate New Account")
        name = input("Enter your name: ").strip()

        while True:
            pin = input("Create a 4-digit PIN: ")
            if pin.isdigit() and len(pin) == 4:
                break
            print("PIN must be 4 digits. Please try again.")

        while True:
            try:
                balance = float(input("Enter initial deposit amount: $"))
                if balance > 0:
                    break
                else:
                    print("Amount must be positive.")
            except ValueError:
                print("Invalid amount. Try again.")

        acc_num = self.generate_account_number()
        account = Account(acc_num, pin, name, balance)
        account.save()
        account.log_transaction(f"Account created with balance ${balance:.2f}")
        print(f"\nAccount created successfully!\nYour account number is: {acc_num}")

    def login(self):
        print("\nATM Login")
        acc_num = input("Enter account number: ").strip()
        pin = input("Enter PIN: ").strip()

        account = Account.get(acc_num)
        if account and account.pin == pin:
            self.current_account = account
            print(f"\nWelcome, {account.name}!")
            self.show_main_menu()
        else:
            print("Invalid credentials.")

    def show_main_menu(self):
        while self.current_account:
            print("\nATM Menu:")
            print("1. Check Balance")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Transfer Money")
            print("5. Transaction History")
            print("6. Change PIN")
            print("7. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.show_transaction_history()
            elif choice == "6":
                self.change_pin()
            elif choice == "7":
                print("Logging out...")
                self.current_account = None
            else:
                print("Invalid choice.")

    def check_balance(self):
        print(f"\nBalance: ${self.current_account.balance:.2f}")

    def withdraw(self):
        try:
            amount = float(input("\nEnter amount to withdraw: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if amount > self.current_account.balance:
                print("Insufficient balance.")
                return
            
            # Update balance in database first
            new_balance = self.current_account.balance - amount
            self.current_account.update_balance(new_balance)
            self.current_account.log_transaction(f"Withdrawal: -${amount:.2f}")
            print("Withdrawal successful.")
        except ValueError:
            print("Invalid input.")

    def deposit(self):
        try:
            amount = float(input("\nEnter amount to deposit: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            # Update balance in database first
            new_balance = self.current_account.balance + amount
            self.current_account.update_balance(new_balance)
            self.current_account.log_transaction(f"Deposit: +${amount:.2f}")
            print("Deposit successful.")
        except ValueError:
            print("Invalid input.")

    def transfer(self):
        recipient_acc = input("\nEnter recipient's account number: ").strip()

        if recipient_acc == self.current_account.account_number:
            print("Cannot transfer to your own account.")
            return

        recipient = Account.get(recipient_acc)
        if not recipient:
            print("Recipient account not found.")
            return

        try:
            amount = float(input("Enter amount to transfer: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if amount > self.current_account.balance:
                print("Insufficient funds.")
                return

            # Start transaction
            with sqlite3.connect("atm.db") as conn:
                try:
                    # Update sender balance
                    sender_new_balance = self.current_account.balance - amount
                    conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                                (sender_new_balance, self.current_account.account_number))
                    
                    # Update recipient balance
                    recipient_new_balance = recipient.balance + amount
                    conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                                (recipient_new_balance, recipient.account_number))
                    
                    # Log transactions
                    conn.execute("INSERT INTO transactions (account_number, details) VALUES (?, ?)",
                               (self.current_account.account_number, f"Transfer to {recipient_acc}: -${amount:.2f}"))
                    conn.execute("INSERT INTO transactions (account_number, details) VALUES (?, ?)",
                               (recipient.account_number, f"Transfer from {self.current_account.account_number}: +${amount:.2f}"))
                    
                    # Commit transaction
                    conn.commit()
                    
                    # Update local objects
                    self.current_account.balance = sender_new_balance
                    recipient.balance = recipient_new_balance
                    
                    print("Transfer successful.")
                except Exception as e:
                    conn.rollback()
                    print("Transfer failed. Please try again.")
                    print(f"Error: {str(e)}")
        except ValueError:
            print("Invalid input.")

    def show_transaction_history(self):
        transactions = Account.get_transactions(self.current_account.account_number)
        print(f"\nTransaction History for {self.current_account.account_number}")
        if not transactions:
            print("No transactions.")
        else:
            for detail, timestamp in transactions:
                print(f"[{timestamp}] {detail}")

    def change_pin(self):
        new_pin = input("\nEnter new 4-digit PIN: ")
        if not (new_pin.isdigit() and len(new_pin) == 4):
            print("PIN must be 4 digits.")
            return
        confirm = input("Confirm new PIN: ")
        if new_pin == confirm:
            self.current_account.change_pin(new_pin)
            print("PIN changed successfully.")
        else:
            print("PINs do not match.")


def main():
    atm = ATM()
    while True:
        print("\nWelcome to the ATM System")
        print("1. Login")
        print("2. Create New Account")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            atm.login()
        elif choice == "2":
            atm.create_account()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
