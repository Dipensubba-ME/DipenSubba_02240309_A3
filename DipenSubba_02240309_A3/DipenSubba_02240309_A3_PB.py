import unittest
from DipenSubba_02240309_A3_PA import (
    BankAccount, PersonalAccount, BusinessAccount,
    InvalidInputError, TransferError, BankSystem
)

class TestBankingApplication(unittest.TestCase):
    """
    This class tests the banking application functions
    like deposit, withdraw, transfer, top-up, and login.
    """

    def setUp(self):
        """
        This method runs before every test.
        It creates two accounts: one personal and one business.
        """
        self.personal = PersonalAccount("10001", "1234", 500.0)
        self.business = BusinessAccount("20001", "4321", 1000.0)



    def test_deposit_negative(self):
        """
        Test that depositing a negative amount raises an error.
        """
        with self.assertRaises(InvalidInputError):
            self.personal.deposit(-100)

    def test_withdraw_excessive(self):
        """
        Test that withdrawing more than the balance raises an error.
        """
        with self.assertRaises(InvalidInputError):
            self.personal.withdraw(1000)

    def test_top_up_invalid_number(self):
        """
        Test that topping up an invalid phone number raises an error.
        """
        with self.assertRaises(InvalidInputError):
            self.personal.top_up_mobile("12345", 50)

    def test_top_up_insufficient_balance(self):
        """
        Test that topping up with more than the balance raises an error.
        """
        with self.assertRaises(InvalidInputError):
            self.personal.top_up_mobile("12345678", 9999)



    def test_transfer_invalid_account(self):
        """
        Test that transferring to a non-BankAccount object raises an error.
        """
        with self.assertRaises(TransferError):
            self.personal.transfer(100, "Invalid_account")

    def test_transfer_insufficient_balance(self):
        """
        Test that transferring more than the balance raises an error.
        """
        with self.assertRaises(InvalidInputError):
            self.personal.transfer(1000, self.business)

    

    def test_valid_deposit(self):
        """
        Test depositing a valid amount updates the balance correctly.
        """
        msg = self.personal.deposit(200)
        self.assertEqual(self.personal.balance, 700.0)
        self.assertEqual(msg, "Deposit successful.")

    def test_valid_withdraw(self):
        """
        Test withdrawing a valid amount updates the balance correctly.
        """
        msg = self.personal.withdraw(100)
        self.assertEqual(self.personal.balance, 400.0)
        self.assertEqual(msg, "Withdrawal successful.")

    def test_valid_transfer(self):
        """
        Test a valid transfer between accounts updates both balances.
        """
        self.personal.transfer(200, self.business)
        self.assertEqual(self.personal.balance, 300.0)
        self.assertEqual(self.business.balance, 1200.0)

    def test_valid_top_up(self):
        """
        Test a valid mobile top-up reduces the account balance correctly.
        """
        msg = self.personal.top_up_mobile("98765432", 100)
        self.assertEqual(self.personal.balance, 400.0)
        self.assertIn("Mobile top-up", msg)

    

    def test_account_creation(self):
        """
        Test that a new account is created and added to the system.
        """
        system = BankSystem(filename="test_accounts.txt")
        acc = system.create_account("Personal")
        self.assertIn(acc.account_id, system.accounts)

    def test_login_invalid(self):
        """
        Test that logging in with wrong credentials raises an error.
        """
        system = BankSystem(filename="test_accounts.txt")
        with self.assertRaises(InvalidInputError):
            system.login("error id", "no pass")

if __name__ == '__main__':
    unittest.main()
