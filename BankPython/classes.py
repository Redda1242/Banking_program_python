from datetime import date


class CustomerAge:
    def __init__(self, year: int, month: int, day: int):
        """ Initiate year (int) , month(int) and day (day)"""

        self.day = int(day)
        self.month = int(month)
        self.year = int(year)
        self.date_of_birth = date(self.year, self.month, self.day)

    def __str__(self) -> str:
        return "date of birth:" + str(self.date_of_birth)

    def age(self) -> int:
        """
            Calculate the age using birthday.

            Return:
            age (int)

            References:
            https://www.codingem.com/how-to-calculate-age-in-python/
        """
        # Get today's date
        today = date.today()

        # check if today's date is before or after birth day and month and save it as bool
        check_date = ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

        # find years differance
        year_difference = today.year - self.date_of_birth.year

        # to get age, subtract check ( 1 or 0) from the year difference
        age = year_difference - check_date

        return age


class Customer(object):
    def __init__(self, identification: str, first_name: str, last_name: str, phone_number: str,
                 year: int, month: int, day: int):
        """ Initiate parameters"""
        self.id = identification
        self.first_name = first_name
        self.last_name = last_name
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)
        self.phone_number = phone_number
        self._pin = ''

    def get_pin(self) -> str:
        """ Function to get value of _pin. Privately."""
        return self._pin

    def set_pin(self, a: str):
        """ Function to set value of _age."""
        self._pin = a

    def __str__(self) -> str:
        """Function to return string of customer data."""
        return "\nName: " + self.first_name + " " + self.last_name + "\ndate of birth: " + \
               str(self.day) + "/" + str(self.month) + "/" + str(self.year) + "\n Phone number: " + self.phone_number


class BankAccount(object):
    """Creates a bank account and allow different transactions on it"""
    def __init__(self, customer_id: str, account_type: str, iban: str, funds: int, withdrawals: int,
                 transfers: int, year: int, month: int, day: int):
        """Initiate Parameters and call the class CustomerAge()"""
        self.IBAN = iban
        self.customer_id = customer_id
        self.withdrawals = withdrawals
        self.transfers = transfers
        self.account_type = account_type
        self.funds = funds
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    def __str__(self) -> str:
        """ Return string of the class data"""
        result = "IBAN: " + self.IBAN + "\n"
        result += "Funds:" + str(self.funds) + "\n" + "Account Type:" + self.account_type

        return result

    def withdraw(self, amount: int):
        """Withdraw money from bank account by a specific amount."""
        if amount <= 0:
            print("You can only withdraw a positive value")
            return 0
        self.funds -= amount
        self.withdrawals += 1

    def deposit(self, amount: int):
        """Deposit money in an account by a specific amount."""
        if amount <= 0:
            print("You can only deposit a positive value")
            return 0
        self.funds += amount

    def transfer(self, to_account, amount):
        """Transfers Money from one account to another by a specific amount"""
        if amount <= 0:
            print("You can only transfer a positive value")
            return 0

        self.funds -= amount
        to_account.funds += amount

        self.transfers += 1

    def balance(self):
        """Displays funds in an account"""
        print("your balance is \n " + str(self.funds))

    def del_account(self):
        """Delete account"""
        del self


class SavingAccount(BankAccount):
    def __init__(self, customer_id: str, account_type: str, iban: str, funds: int, withdrawals: int,
                 transfers: int, year: int, month: int, day: int):
        """ Initiate parameters and check if customer age is above minimum age to create account."""
        self.day = day
        self.month = month
        self.year = year
        self.obj_age = CustomerAge(self.year, self.month, self.day)
        age = self.obj_age.age()

        # if age is above 14 create class
        if age >= 14:
            super().__init__(customer_id, account_type, iban, funds, withdrawals, transfers, year, month, day)
        else:
            print("Too young to create account")
            return 0

    def withdraw(self, amount: int):
        """
            Withdraw money from account.

            Checking withdrawals and transfers are not more than 1 and amount to withdraw will not cause a negative
            credit.
        """
        # if user did not exceed withdrawals and transfers times do
        if (self.withdrawals + self.transfers) == 0:

            # check user has funds
            if self.funds != 0:

                # check that amount will not cause funds to be negative
                if self.funds - amount > 0:

                    # withdraw (inherit function from BankAccounts)
                    super().withdraw(amount)
                else:
                    print("you do not have enough credit")
                    return 0
            else:
                print("you do not have enough credit")
                return 0
        else:
            print("you can no longer withdraw/transfer from this account this month")
            return 0

    def transfer(self, to_account, amount):
        """Transfers Money to another account"""
        if self.funds == 0:
            print("Failed!.You have reached maximum credit negative score")
            return 0
        elif (self.funds - amount) < 0:
            print("We can not deduct the current amount from you account as your account type does not allow"
                  "negative credit")
            return 0
        elif(self.withdrawals + self.transfers) == 0:
            super().transfer(to_account, amount)
        else:
            print("\nyou can no longer withdraw/transfer from this account this month\n")
            return 0

class CheckingAccount(BankAccount):
    def __init__(self, customer_id: str, account_type: str, iban: str, funds: int, withdrawals: int,
                 transfers: int, year: int, month: int, day: int):
        """Initiate parameters"""
        self.day = day
        self.month = month
        self.year = year
        self.obj_age = CustomerAge(self.year, self.month, self.day)
        age = self.obj_age.age()

        # check that customer age is above or = 18
        if age >= 18:

            # create account
            super().__init__(customer_id, account_type, iban, funds, withdrawals, transfers, year, month, day)
        else:
            print("Too young to create account")

    def transfer(self, to_account, amount):
        """ Transfers Money to another account in the bank system (inherited from BankAccount)"""

        # check that funds have not reached limit
        if self.funds <= -1000:
            print("Failed!.You have reached maximum credit negative score")
            return

        # check that transfer will not cause funds to pass limit
        elif (self.funds - amount) < -1000:
            print("We can not deduct the current amount from you account as you will maximum credit negative score")
            return
        else:
            # transfer money
            super().transfer(to_account, amount)

    def withdraw(self, amount):
        """Withdraw money from account."""

        # check that funds have not reached limit
        if self.funds <= -1000:
            print("Failed!.You have reached maximum credit negative score")
            return

        # check that transfer will not cause funds to pass limit
        elif (self.funds - amount) < -1000:
            print("We can not deduct the current amount from you account as you will maximum credit negative score")
            return
        else:

            # transfer money
            super().withdraw(amount)


class AccountTransactions(object):
    """Class containing the current transaction"""

    def __init__(self, transaction_id: str, iban: str, transaction_type: str, amount: int, to_account=None):
        """Initiate Parameters."""

        self.transaction_id = transaction_id
        self.iban = iban
        self.transaction_type = transaction_type
        self.amount = amount
        self.to_account = to_account

    def __str__(self) -> str:
        """ Return string containing class data"""
        result = "\n Transaction ID: " + self.transaction_id + "\n IBAN: " + self.iban + \
                 "\n Transaction Type: " + self.transaction_type + "\n Amount: " + str(self.amount)

        if self.to_account is not None:
            result += "\n To : " + self.to_account

        return result

    def display(self):
        """Display current transaction (Customer bill)"""
        result = "\n Transaction ID: " + str(self.transaction_id) + \
                 "\n Transaction Type: " + self.transaction_type + "\n Amount: " + str(self.amount)

        if self.to_account is not None:
            result += "\n To : " + self.to_account

        print(result)
