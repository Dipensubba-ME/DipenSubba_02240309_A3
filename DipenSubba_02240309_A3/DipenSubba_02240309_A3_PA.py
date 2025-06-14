import tkinter as tk
from tkinter import messagebox
import random

# Custom Exceptions
class InvalidInputError(Exception):
    pass

class TransferError(Exception):
    pass

# Bank Account Classes
class BankAccount:
    def __init__(self, account_id, password, account_type, balance=0):
        self.account_id = account_id
        self.password = password
        self.account_type = account_type
        self.balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return "Deposit successful."
        raise InvalidInputError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return "Withdrawal successful."
        raise InvalidInputError("Invalid amount or insufficient funds.")

    def transfer(self, amount, other_account):
        if not isinstance(other_account, BankAccount):
            raise TransferError("Recipient account is invalid.")
        self.withdraw(amount)
        other_account.deposit(amount)
        return "Transfer successful."

    def top_up_mobile(self, phone_number, amount):
        if len(phone_number) != 8 or not phone_number.isdigit():
            raise InvalidInputError("Phone number must be 8 digits.")
        if amount <= 0 or amount > self.balance:
            raise InvalidInputError("Top-up amount invalid or insufficient funds.")
        self.balance -= amount
        return f"Mobile top-up of {amount} to {phone_number} successful."

class PersonalAccount(BankAccount):
    def __init__(self, account_id, password, balance=0):
        super().__init__(account_id, password, "Personal", balance)

class BusinessAccount(BankAccount):
    def __init__(self, account_id, password, balance=0):
        super().__init__(account_id, password, "Business", balance)

# Bank System
class BankSystem:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    acc_id, password, acc_type, balance = line.strip().split(",")
                    bal = float(balance)
                    if acc_type == "Personal":
                        acc = PersonalAccount(acc_id, password, bal)
                    else:
                        acc = BusinessAccount(acc_id, password, bal)
                    accounts[acc_id] = acc
        except FileNotFoundError:
            pass
        return accounts

    def save_accounts(self):
        with open(self.filename, "w") as file:
            for acc in self.accounts.values():
                file.write(f"{acc.account_id},{acc.password},{acc.account_type},{acc.balance}\n")

    def create_account(self, acc_type):
        new_id = str(random.randint(10000, 99999))
        new_pass = str(random.randint(1000, 9999))
        if acc_type == "Personal":
            acc = PersonalAccount(new_id, new_pass)
        else:
            acc = BusinessAccount(new_id, new_pass)
        self.accounts[new_id] = acc
        self.save_accounts()
        return acc

    def login(self, acc_id, password):
        acc = self.accounts.get(acc_id)
        if acc and acc.password == password:
            return acc
        raise InvalidInputError("Invalid account ID or password")

    def delete_account(self, acc_id):
        if acc_id in self.accounts:
            del self.accounts[acc_id]
            self.save_accounts()

# GUI Class
class BankGUI:
    def __init__(self, account, bank_system):
        self.account = account
        self.bank_system = bank_system
        self.window = tk.Tk()
        self.window.title(f"{account.account_type} Account - {account.account_id}")
        self.window.geometry("320x450")

        tk.Label(self.window, text=f"Welcome, {account.account_id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.window, text="Enter Amount:").pack()
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.pack()

        tk.Button(self.window, text="Deposit", command=self.deposit).pack(pady=5)
        tk.Button(self.window, text="Withdraw", command=self.withdraw).pack(pady=5)
        tk.Button(self.window, text="Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.window, text="Transfer Money", command=self.open_transfer_window).pack(pady=5)

        tk.Label(self.window, text="Mobile Top-Up:").pack(pady=5)
        tk.Label(self.window, text="Phone Number:").pack()
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.pack()
        tk.Button(self.window, text="Top Up", command=self.top_up).pack(pady=5)

        tk.Button(self.window, text="Exit", command=self.window.destroy).pack(pady=10)
        self.output_label = tk.Label(self.window, text="", fg="blue")
        self.output_label.pack()
        self.window.mainloop()

    def deposit(self):
        try:
            amt = float(self.amount_entry.get())
            msg = self.account.deposit(amt)
            self.bank_system.save_accounts()
            self.output_label.config(text=f"{msg} New Balance Nu: {self.account.balance:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amt = float(self.amount_entry.get())
            msg = self.account.withdraw(amt)
            self.bank_system.save_accounts()
            self.output_label.config(text=f"{msg} New Balance Nu: {self.account.balance:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_balance(self):
        self.output_label.config(text=f"Balance Nu: {self.account.balance:.2f}")

    def top_up(self):
        try:
            phone = self.phone_entry.get()
            amt = float(self.amount_entry.get())
            msg = self.account.top_up_mobile(phone, amt)
            self.bank_system.save_accounts()
            messagebox.showinfo("Top-Up Successful", f"{msg}\nNew Balance: Nu {self.account.balance:.2f}")
            self.output_label.config(text="")
        except Exception as e:
            messagebox.showerror("Top-Up Error", str(e))

    def open_transfer_window(self):
        win = tk.Toplevel(self.window)
        win.title("Transfer Money")
        win.geometry("300x200")

        tk.Label(win, text="Recipient Account ID:").pack(pady=5)
        recv_entry = tk.Entry(win); recv_entry.pack()

        tk.Label(win, text="Amount:").pack(pady=5)
        amt_entry = tk.Entry(win); amt_entry.pack()

        def do_transfer():
            try:
                rid = recv_entry.get().strip()
                amt = float(amt_entry.get())
                if rid not in self.bank_system.accounts:
                    raise TransferError("Recipient not found.")
                recv_acc = self.bank_system.accounts[rid]
                msg = self.account.transfer(amt, recv_acc)
                self.bank_system.save_accounts()
                messagebox.showinfo("Success", f"{msg}\nNew Balance: Nu {self.account.balance:.2f}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Transfer Error", str(e))

        tk.Button(win, text="Transfer", command=do_transfer).pack(pady=10)
        tk.Button(win, text="Cancel", command=win.destroy).pack()

# Login GUI        
class LoginWindow:
    def __init__(self, bank_system):
        self.bank_system = bank_system
        self.window = tk.Tk()
        self.window.title("Bank Login")
        self.window.geometry("300x350")

        tk.Label(self.window, text="Account Type:").pack()
        self.acc_type = tk.StringVar(value="Personal")
        tk.Radiobutton(self.window, text="Personal", variable=self.acc_type, value="Personal").pack()
        tk.Radiobutton(self.window, text="Business", variable=self.acc_type, value="Business").pack()

        tk.Label(self.window, text="Account ID:").pack()
        self.acc_entry = tk.Entry(self.window)
        self.acc_entry.pack()
        tk.Label(self.window, text="Password:").pack()
        self.pass_entry = tk.Entry(self.window, show="*")
        self.pass_entry.pack()

        tk.Button(self.window, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.window, text="Create Account", command=self.create_account).pack(pady=5)
        tk.Button(self.window, text="Exit", command=self.window.destroy).pack(pady=10)

        self.window.mainloop()

    def login(self):
        try:
            acc = self.bank_system.login(self.acc_entry.get().strip(), self.pass_entry.get().strip())
            self.window.destroy()
            BankGUI(acc, self.bank_system)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def create_account(self):
        acc = self.bank_system.create_account(self.acc_type.get())
        messagebox.showinfo("Account Created", f"ID: {acc.account_id}\nPassword: {acc.password}")

if __name__ == "__main__":
    system = BankSystem()
    LoginWindow(system)
