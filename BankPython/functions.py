def retrieve_data(accounts_dictionary: dict, customers_dictionary: dict, account_transactions: dict) -> tuple:
    """
            Read the data from the accounts, customers and transactions file and store
            them in 3 different dictionaries.
    """
    # read files from the current directory
    accounts_file = open("accounts.txt")
    customers_file = open("customers.txt")
    account_transactions_file = open("accountTransactions.txt")

    # add the data from the accounts file to the dictionary
    for line in accounts_file:
        try:
            (key, *values) = line.split()
            accounts_dictionary[key] = values

        # if the file is empty ignore error
        except ValueError:
            pass

    # read data from customer file into the dictionary
    for line in customers_file:
        try:
            (key, *values) = line.split()
            customers_dictionary[key] = values

        # if the file is empty ignore error
        except ValueError:
            pass

    # read data from the transaction file in the dictionary
    for line in account_transactions_file:
        try:
            (key, *values) = line.split()
            account_transactions[key] = values

        # if the file is empty ignore error
        except ValueError:
            pass

    accounts_file.close()
    customers_file.close()
    account_transactions_file.close()

    return accounts_dictionary, customers_dictionary, account_transactions


def login(login_check: int, customers: dict) -> tuple:
    """
        Function to allow user to Login to the bank system.

        User is asked to enter their credentials (customer ID and pin number),
        The function checks if the credentials are correct and allow login, Otherwise
        customer needs to re enter credentials.

        Parameters:
        login_check (int): Has the login status, 1 for logged in and 0 for logged out.
        customers (dict): customers dictionary containing data of all customers

        Returns:
        entered_customer_id (str)
        first_name (str)
        last_name (str)
        phonenumber (str)
        birth_year (int)
        birth_month (int)
        birth_day (int)
    """
    while True:

        # Ask user to enter their ID and pin number
        entered_customer_id = input("\n Please enter your customer ID\n")
        user_pin = input("\n Please enter your 4 digits PIN\n")

        # iterate through customers dictionary to find the ID the user entered
        for customer_key, customer_pin in customers.items():

            # if id is found,  check if pin is associated with it
            if entered_customer_id == customer_key:
                if user_pin == customer_pin[3]:

                    # inform user
                    print("\n Login successful")

                    # change login status to 1
                    login_check = 1

                    break

        # if logged in iterate through dictionary keys and values to retrieve user name and age
        if login_check == 1:
            for customer_key, customer_values in customers.items():
                if entered_customer_id == customer_key:
                    first_name = customer_values[0]
                    last_name = customer_values[1]
                    phonenumber = customer_values[2]
                    birth_year = customer_values[4]
                    birth_month = customer_values[5]
                    birth_day = customer_values[6]
                    return entered_customer_id, first_name, last_name, phonenumber, birth_year, birth_month, birth_day

        else:
            try_again = input("\n login failed, Would you like to try again?(y/n)\n")
            if try_again == 'n' or try_again == 'N':
                return


def update_file(accounts: dict, account_transactions: dict, customers: dict):
    """
            Function to update the the files in current directory with the updated dictionaries. The dictionaries are
            over written in the files with out the brackets and and commas.

            parameters:
            accounts (dict)
            account_transactions (dict)
            customers (dict)
    """

    # write accounts dictionary in accounts.txt stripping brackets and commas
    with open("accounts.txt", 'w') as f:
        for keys, value in accounts.items():
            f.write('%s %s\n' % (keys, str(value).strip('[]').replace(',', '').replace('\'', '')))

    # close file
    f.close()

    # write accountTransactions dictionary in accountsTransaction.txt stripping brackets and commas
    with open("accountTransactions.txt", 'w') as f:
        for keys, value in account_transactions.items():
            f.write('%s %s\n' % (keys, str(value).strip('[]').replace(',', '').replace('\'', '')))

    # close file
    f.close()

    # write customers dictionary in customers.txt stripping brackets and commas
    with open("customers.txt", 'w') as f:
        for keys, value in customers.items():
            f.write('%s %s\n' % (keys, str(value).strip('[]').replace(',', '').replace('\'', '')))

    # close file
    f.close()


def service_menu() -> str:
    """
            Function to allow user to choose from services menu and return user's choice.

            return :
            user_choice (str)
    """
    while True:
        user_choice = input(
            "What would you like to do\n"
            "1.View balance\n"
            "2.Deposit\n"
            "3.Transfer\n"
            "4.Withdraw\n"
            "5.View transaction history\n"
            "6.Delete Account\n"
            "7.Back to main menu\n")

        return user_choice
