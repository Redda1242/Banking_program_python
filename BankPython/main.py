# Import classes from classes files

from classes import SavingAccount
from classes import CheckingAccount
from classes import AccountTransactions
from classes import Customer
from functions import retrieve_data, update_file, service_menu, login

# import random to create random numbers for unique values
import random

# declare dictionaries for data
accounts = {}
customers = {}
accountTransactions = {}

# declare variables
iban = ''
account_type = ''
account_funds = 0
account_withdrawals = 0
account_transfers = 0
account_year = 0
account_month = 0
account_day = 0
account_created = 0
to_account_type = ''
to_account_funds = 0
to_account_withdrawals = 0
to_account_transfers = 0
to_account_year = 0
to_account_month = 0
to_account_day = 0
to_account_customer_id = ''

# to check login status
login_status = 0

# exit
exit_program = 0

# ---------------------------------------MAIN------------------------------------------------------------------

# retrieve data from files to dictionaries
accounts, customers, accountTransactions = retrieve_data(accounts, customers, accountTransactions)

while True:

    while True:
        # ask user if they are a new customer
        new_customer = input("\n Are you a new customer?(Y/N) \n")

        # if yes, ask user for their details and create new customer using Customer class
        if new_customer == 'Y' or new_customer == 'y':

            # ask for new id
            customer_id = input("\n Please enter a new customer ID\n")

            # if id already exist inform user
            while True:
                if customer_id in customers.keys():
                    customer_id = input("\nID already exist please enter a new ID\n")
                else:
                    break

            # ask for first name
            firstname = input("\n Enter your first name\n")

            # ask for last name
            lastname = input("\n Enter your last name\n")

            # ask for pin
            pin = input("\n Please enter your new 4 digits pin\n")

            # check pin is not longer than 4 characters
            while True:
                if len(pin) > 4:
                    pin = input("\n Please enter a new pin with ONLY 4 DIGITS\n")
                else:
                    break

            # ask user for date of birth
            year = int(input('Enter year you were born'))

            while True:
                if year < 1900 or year > 2015:
                    year = int(input("\n Please enter a relevant data (YYYY)\n"))
                else:
                    break

            month = int(input(' Enter month you were born'))

            while True:
                if month < 0 or month > 12:
                    month = int(input("\n Please enter a relevant month 1-12 (MM)\n"))
                else:
                    break

            day = int(input('Enter day you were born in'))

            while True:
                if day < 1 or day > 31:
                    day = int(input("\n Please enter a relevant day 1-31\n"))
                else:
                    break

            # ask user for phone number
            phone_number = input("\n Please enter your phone number\n")

            # create new customer using class
            registered_customer = Customer(customer_id, firstname, lastname, phone_number, year, month, day)

            # set pin for customer
            registered_customer.set_pin(pin)

            # add new customer to the customers dictionary
            customers[registered_customer.id] = [registered_customer.first_name, registered_customer.last_name,
                                                 registered_customer.phone_number, registered_customer.get_pin(),
                                                 registered_customer.year, registered_customer.month,
                                                 registered_customer.day]

            # update the files
            update_file(accounts, accountTransactions, customers)

            break

        elif new_customer == 'N' or new_customer == 'n':
            # ask user to login
            try:
                customer_id, firstname, lastname, phone_number,\
                    year, month, day = login(login_status, customers)
                break
            except TypeError:
                pass
        else:
            print("\nInvalid input\n")

    # run main menu
    while True:
        transaction_status = 1
        print("\nWelcome " + firstname)
        current_customer = Customer(customer_id, firstname, lastname, phone_number, year, month, day)
        choice = input("\n"
                       "What would you like to do\n"
                       "1.Create New Account\n"
                       "2.Account services\n"
                       "3.exit\n")

        # create account
        if choice == '1':

            while True:

                # ask user for account type checking or saving
                accountType = \
                    input(
                        "\nWhat Account type would you like to create?\n "
                        "1.Checking\n"
                        "2.Saving\n "
                        "3.Back to main menu\n")

                if accountType == '1':

                    # create new IBAN for the new account
                    IBAN = "IE" + \
                           str(random.randrange(10, 100))\
                           + "IRE" + str(random.randrange(10000000000000, 100000000000000))

                    # create account
                    acc = CheckingAccount(customer_id, "checking", IBAN, 0, 0, 0, year, month, day)

                    try:
                        # add account to accounts dictionary
                        accounts[acc.IBAN] = [acc.customer_id, acc.account_type, acc.funds,
                                              acc.withdrawals, acc.transfers, acc.year, acc.month, acc.day]

                        # inform user
                        print("\n your account was successfully created\n")

                    except AttributeError:
                        print("\nfailed to create account\n")

                    # update files
                    update_file(accounts, accountTransactions, customers)

                elif accountType == '2':

                    # create new account IBAN
                    IBAN = "IE" + str(random.randrange(10, 100)) + "IRE" + \
                           str(random.randrange(10000000000000, 100000000000000))

                    # create account
                    acc = SavingAccount(customer_id, "saving", IBAN, 0, 0, 0, year, month, day)

                    try:
                        # add account to accounts dictionary
                        accounts[acc.IBAN] = [acc.customer_id, acc.account_type, acc.funds,
                                              acc.withdrawals, acc.transfers, acc.year, acc.month, acc.day]

                        # inform user
                        print("\n your account was successfully created\n")

                    except AttributeError:
                        print("\nfailed to create account\n")

                    # update files
                    update_file(accounts, accountTransactions, customers)

                elif accountType == '3':
                    break

                # validate user input
                else:
                    print("\n You entered an invalid number")

        elif choice == '2':

            # iterate through the accounts which have the customer ID and print them
            print("\n These are your accounts\n")
            index = 0
            for keys, value_dic in accounts.items():
                if customer_id in value_dic:
                    index += 1
                    iban = keys
                    print(index, ":", keys, value_dic[0], value_dic[1], value_dic[2])

            # if there is more than one account, ask user which account they would like to perform on
            if index > 1:
                account_iban = input("\nEnter IBAN of the account you would like to perform on?\n")

            # else if there is only one account
            elif index == 1:
                account_iban = iban

            # if the customer has no accounts, inform them and return to main
            else:
                print("\nYou do not have and account Please create an account first (Logging out)\n")
                break

            # iterate through the accounts dictionary and retrieve accounts data
            for keys, value_dic in accounts.items():
                if account_iban in keys:
                    customer_id = value_dic[0]
                    account_type = value_dic[1]
                    account_funds = value_dic[2]
                    account_withdrawals = value_dic[3]
                    account_transfers = value_dic[4]
                    account_year = int(value_dic[5])
                    account_month = int(value_dic[6])
                    account_day = int(value_dic[7])

                    break

            try:
                # create account using classes CheckingAccount and SavingAccount to use class functions
                if account_type == "checking":
                    current_account = CheckingAccount(customer_id, account_type, account_iban,
                                                      int(account_funds), int(account_withdrawals),
                                                      int(account_transfers), account_year, account_month, account_day)
                    account_created = 1
                else:
                    current_account = SavingAccount(customer_id, account_type, account_iban,
                                                    int(account_funds), int(account_withdrawals),
                                                    int(account_transfers), account_year, account_month, account_day)
                    account_created = 1
            except UnboundLocalError:
                pass

            # if account is created show menu
            if account_created == 1:

                # print service menu
                option = service_menu()

                # perform service according to user's option
                if option == '1':

                    # print balance using class function
                    current_account.balance()

                elif option == '2':

                    # Ask user for amount of money
                    deposit_money = int(input("\nHow much would you like to deposit\n"))

                    # deposit money using class function
                    current_account.deposit(deposit_money)

                    # update data in the dictionary
                    accounts[current_account.IBAN] = \
                        [current_account.customer_id, current_account.account_type, current_account.funds,
                         current_account.withdrawals, current_account.transfers, current_account.year,
                         current_account.month, current_account.day]

                    # create a new transaction ID
                    transaction_id = str(random.randrange(100, 500))

                    # create transaction using accountTransactions class
                    transaction = AccountTransactions(transaction_id, current_account.IBAN, "deposit", deposit_money)

                    # add transaction to the accountTransactions dictionary
                    accountTransactions[transaction.transaction_id] = \
                        [transaction.iban, transaction.transaction_type, transaction.amount]

                    # call update_file function to update files to new data
                    update_file(accounts, accountTransactions, customers)

                    # ask user if they would like a receipt
                    receipt = input("\nWould you like a receipt?(Y/N)\n")
                    if receipt == 'Y' or receipt == 'y':
                        transaction.display()

                elif option == '3':

                    # ask user for the account's IBAN they want to transfer money to and the receiver name
                    transfer_iban = input("\nEnter account's IBAN\n")
                    to_user_name = input("\nEnter Name of the user you would like to transfer to\n")

                    # iterate through accounts dictionary to check for iban and  if found retrieve account data
                    count = 0
                    for keys, value_dic in accounts.items():
                        if transfer_iban in keys:
                            to_account_customer_id = value_dic[0]
                            to_account_type = value_dic[1]
                            to_account_funds = value_dic[2]
                            to_account_withdrawals = value_dic[3]
                            to_account_transfers = value_dic[4]
                            to_account_year = int(value_dic[5])
                            to_account_month = int(value_dic[6])
                            to_account_day = int(value_dic[7])
                            count += 1
                            break

                    # if account was found
                    if count > 0:

                        # create account using class according to the account type
                        if account_type == "checking":

                            to_account = CheckingAccount(to_account_customer_id, to_account_type, transfer_iban,
                                                         int(to_account_funds), int(to_account_withdrawals),
                                                         int(to_account_transfers),
                                                         to_account_year, to_account_month, to_account_day)

                        elif account_type == "saving":
                            to_account = SavingAccount(to_account_customer_id, to_account_type, transfer_iban,
                                                       int(to_account_funds), int(to_account_withdrawals),
                                                       int(to_account_transfers),
                                                       to_account_year, to_account_month, to_account_day)

                        # ask user how much money they would like to transfer
                        transfer_money = int(input("\nHow much would you like to transfer\n"))

                        # transfer money using Account class function
                        transaction_status = current_account.transfer(to_account, transfer_money)

                        if transaction_status != 0:
                            # update dictionary with new amounts for the customer
                            accounts[current_account.IBAN] = \
                                [current_account.customer_id, current_account.account_type, current_account.funds,
                                 current_account.withdrawals, current_account.transfers, current_account.year,
                                 current_account.month, current_account.day]

                            # and receiver account
                            accounts[to_account.IBAN] = [to_account.customer_id, to_account.account_type, to_account.funds,
                                                         to_account.withdrawals, to_account.transfers,
                                                         to_account.year, to_account.month, to_account.day]

                            # make transaction ID for current customer
                            transaction_id = str(random.randrange(100, 500))

                            # create transaction
                            transaction = AccountTransactions(transaction_id, current_account.IBAN, "transfer",
                                                              transfer_money, to_account.IBAN)

                            # add transaction in dictionary
                            accountTransactions[transaction.transaction_id] = \
                                [transaction.iban, transaction.transaction_type,
                                 transaction.amount, transaction.to_account]

                            # make transaction id for receiver
                            to_account_transaction_id = str(random.randrange(100, 500))

                            # create transaction
                            transaction_to_account = AccountTransactions(to_account_transaction_id,
                                                                         to_account.IBAN, "Added", transfer_money,
                                                                         current_account.IBAN)

                            # add transaction to the dictionary
                            accountTransactions[transaction_to_account.transaction_id] = \
                                [transaction_to_account.iban, transaction_to_account.transaction_type,
                                 transaction_to_account.amount, transaction_to_account.to_account]

                            # update all files
                            update_file(accounts, accountTransactions, customers)

                            # ask user if they would like a receipt
                            receipt = input("\nWould you like a receipt?(Y/N)\n")
                            if receipt == 'Y' or receipt == 'y':
                                transaction.display()

                    # if account is not found inform user
                    else:
                        print("\n Sorry the IBAN you entered does not exist in the system\n")

                elif option == '4':

                    # ask user for amount of money they would like to withdraw
                    withdraw_money = int(input("\nHow much would you like to withdraw\n"))

                    # withdraw using BankAccount class function
                    transaction_status = current_account.withdraw(withdraw_money)

                    if transaction_status != 0:
                        # update dictionary
                        accounts[current_account.IBAN] = [current_account.customer_id, current_account.account_type,
                                                          current_account.funds, current_account.withdrawals,
                                                          current_account.transfers, current_account.year,
                                                          current_account.month, current_account.day]

                        # create transaction
                        transaction_id = str(random.randrange(100, 500))
                        transaction = AccountTransactions(transaction_id, current_account.IBAN, "withdraw", withdraw_money)

                        # and add it to the accountTransactions dictionary
                        accountTransactions[transaction.transaction_id] = \
                            [transaction.iban, transaction.transaction_type, transaction.amount]

                        # update the files
                        update_file(accounts, accountTransactions, customers)

                        # ask user if they would like a receipt
                        receipt = input("\nWould you like a receipt?(Y/N)\n")
                        if receipt == 'Y' or receipt == 'y':
                            transaction.display()

                elif option == '5':

                    # iterate through accountTransactions and print all transactions from the current iban
                    for keys, values_list in accountTransactions.items():
                        if current_account.IBAN in values_list:
                            print(accountTransactions[keys])

                elif option == '6':
                    delete_keys = []
                    # pop transactions of the deleted account
                    for keys, value in accountTransactions.items():
                        if current_account.IBAN == value[0]:
                            delete_keys.append(keys)

                    for values in delete_keys:
                        accountTransactions.pop(values)

                    # pop the iban from accounts dictionary
                    accounts.pop(current_account.IBAN)
                    print('\nAccount was successfully deleted')

                    # delete
                    current_account.del_account()

                    # update files
                    update_file(accounts, accountTransactions, customers)
                    break

                elif option == '7':
                    # exit
                    break

                # check user input
                else:
                    print("invalid input")
            else:
                print("Failed to retrieve account")

        elif choice == '3':

            # exit program
            exit_program = 1
            break
        else:
            print("invalid input")

    if exit_program == 1:
        print("\n Program ends now\n")
        break
