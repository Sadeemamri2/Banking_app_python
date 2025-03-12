import csv
from datetime import datetime
##########################################  CLASS BANK_DATA  ###############################################

# The Bank_data class is responsible for loading and saving customer data from/to a CSV file.

class Bank_data:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        customers = []
        with open(self.filename, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if not any(customer[0] == row[0] for customer in customers):
                    customers.append(row)
        return customers

    def save_data(self, customers):
        with open(self.filename, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(customers)

##########################################  CLASS CUSTOMER  ###############################################

# The Customer class represents a bank account with attributes like account_id, balances, and password.
# It provides methods to check passwords, apply overdraft fees, and manage account activation and deactivation.
# The overdraft limit is set to -$100, and accounts can be reactivated with a cleared balance and reset overdraft count.

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking, balance_savings, overdraft_count=0, account_active=True):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking)
        self.balance_savings = float(balance_savings)
        self.overdraft_count = overdraft_count  
        self.account_active = account_active  

    def check_password(self, entered_password):
        return self.password == entered_password

    def apply_overdraft_fee(self):
        self.balance_checking -= 35  
        print(f"❌ Overdraft fee of $35 applied to account {self.account_id}")

    def check_overdraft(self, amount):
        if self.balance_checking + amount < -100:
            return False  
        return True

    def deactivate_account(self):
        self.account_active = False  
        print(f"❌ Account {self.account_id} deactivated due to overdraft limit exceeded.")

    def reactivate_account(self):
        self.account_active = True  
        self.balance_checking = 0  
        self.overdraft_count = 0  
        print(f"✅ Account {self.account_id} reactivated and balance cleared.")

##########################################  CLASS BANK_ACCOUNT  ###############################################

# The Account class manages a customer's account operations such as deposit, withdrawal, transfer, and overdraft handling.
# It allows deposits, withdrawals with overdraft fees, and transfers between checking and savings accounts, or to other customers.
# The class also tracks overdraft occurrences and deactivates the account after two overdrafts.


class Account:
    def __init__(self, customer):
        self.customer = customer

    def deposit(self, amount):
        self.customer.balance_checking += amount

    def withdraw(self, amount):
       
        if self.customer.balance_checking < 0:
            self.customer.balance_checking -= 35  
            print("❌ Overdraft fee applied!")

       
        if self.customer.balance_checking - amount < -100:
            print("❌ You cannot withdraw more than $100 if your account is negative!")
            return False

        
        if self.customer.balance_checking >= amount:
            self.customer.balance_checking -= amount
            return True
        else:
            print("❌ Insufficient funds!")
            return False

    def transfer(self, amount, from_checking_to_savings):
        if from_checking_to_savings:  
            if self.customer.balance_checking >= amount:
                self.customer.balance_checking -= amount
                self.customer.balance_savings += amount
                return True
        else:  
            if self.customer.balance_savings >= amount:
                self.customer.balance_savings -= amount
                self.customer.balance_checking += amount
                return True
        return False

    def transfer_to_other_customer(self, amount, recipient, from_checking_to_savings, from_checking_to_checking):
        
        if from_checking_to_checking:
            if self.customer.balance_checking >= amount:
                self.customer.balance_checking -= amount
                recipient.balance_checking += amount  
                return True
        elif from_checking_to_savings: 
            if self.customer.balance_savings >= amount:
                self.customer.balance_savings -= amount
                recipient.balance_checking += amount  
                return True
        return False

    def handle_overdraft(self):
        if self.customer.balance_checking < 0:
            self.customer.overdraft_count += 1
            self.customer.apply_overdraft_fee()
            if self.customer.overdraft_count >= 2:
                self.customer.deactivate_account()  

##########################################  CLASS TRANSACTION  ###############################################

# The Transaction class handles various account actions such as deposits, withdrawals, and transfers.
# It supports depositing money into checking, withdrawing from checking, and transferring between checking and savings or to other customers.
# It also prints the result of each action, including success or failure messages based on available funds.


class Transaction:
    def __init__(self, account):
        self.account = account
    
    def log_transaction(self, action, amount):
        """تسجيل العملية في ملف transactionLog.csv"""
        with open("transactionLog.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),  # التاريخ
                datetime.now().strftime("%H:%M:%S"),  # الوقت
                self.account.customer.account_id,     # رقم الحساب
                action,                               # نوع العملية
                amount,                               # المبلغ
                self.account.customer.balance_checking  # الرصيد بعد العملية
            ])

    def execute(self, action, amount, to_account=None, from_checking_to_savings=False):
        if action == 'deposit':
            self.account.deposit(amount)
            self.log_transaction(action, amount)
            print(f"✅ Deposited ${amount} into checking account.")
        
        elif action == 'withdraw':
            if self.account.withdraw(amount):
                self.log_transaction(action, amount)
                print(f"✅ Withdrew ${amount} from checking account.")
            else:
                print("❌ Insufficient funds!")
        
        elif action == 'transfer':
            if to_account:  
                if self.account.transfer_to_other_customer(amount, to_account, from_checking_to_savings, from_checking_to_checking):

                    from_account_type = "checking" if from_checking_to_checking else "savings" if from_checking_to_savings else "unknown"
                    self.log_transaction("transfer", amount)
                    print(f"✅ ${amount} transferred from {self.account.first_name} {self.account.last_name}'s {from_account_type} account to {to_account.first_name} {to_account.last_name}'s account.")
                else:
                    print("❌ Transfer failed! Insufficient funds.")
            else:  
                if self.account.transfer(amount, from_checking_to_savings):
                    self.log_transaction("transfer", amount)
                    if from_checking_to_savings:
                        print(f"✅ ${amount} transferred from {self.account.first_name}'s checking account to savings.")
                    else:
                        print(f"✅ ${amount} transferred from {self.account.first_name}'s savings account to checking.")
                else:
                    print("❌ Transfer failed! Insufficient funds.")


##################################### MAIN FUNCTION <is the core engine of the program >
def main():
    bank_data = Bank_data('bank1.csv')
    customers = bank_data.load_data()
# to make sure the coustmer object contan the loaded data 
    # print(customers)

# This loop presents a menu to the user for various banking operations, allowing them to choose an action.

    logged_in_customer = None

    while True:
        print("\n WELCOME IN TITAN BANK \n")
        print("\nPlease choose an operation:")
        print("1. Add New Account")
        print("2. Check Account Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Reactivate Account")
        print("7. Exit")

        action = input("Enter the number of the operation: ")


# This code handles adding a new customer account, including account type selection and balance input, 
# and saves the new customer data after validation.

        if action == '1':
            try:
                print("\nAdding New Account:")
                account_id = input("Enter account ID: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                password = input("Enter password: ")

                print("Select account type:")
                print("1. Checking Account")
                print("2. Savings Account")
                print("3. Both")

                account_type = input("Enter choice (1/2/3): ")

                if account_type == '1':
                    balance_checking = float(input("Enter checking account balance: "))
                    balance_savings = 0.0
                elif account_type == '2':
                    balance_savings = float(input("Enter savings account balance: "))
                    balance_checking = 0.0
                elif account_type == '3':
                    balance_checking = float(input("Enter checking account balance: "))
                    balance_savings = float(input("Enter savings account balance: "))
                else:
                    print("❌ Invalid choice. Defaulting to both accounts with 0 balance.")
                    balance_checking, balance_savings = 0.0, 0.0

                new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings)
                customers.append([new_customer.account_id, new_customer.first_name, new_customer.last_name, new_customer.password, new_customer.balance_checking, new_customer.balance_savings, new_customer.overdraft_count, new_customer.account_active])
                bank_data.save_data(customers)
                print(f"✅ New account for {new_customer.first_name} {new_customer.last_name} has been added.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid number for balance.")


# This code handles user login by verifying account ID and password, 
# ensures the account is active, and creates instances for account and transaction if login is successful.

        elif action in ['2', '3', '4', '5', '6']:
            if not logged_in_customer:
                account_id = input("Enter account ID: ")
                password = input("Enter password: ")

                for customer in customers:
                    if customer[0] == account_id:
                        logged_in_customer = Customer(*customer)
                        if not logged_in_customer.check_password(password):
                            print("❌ Incorrect password!")
                            logged_in_customer = None
                        break
                else:
                    print("❌ Account not found!")
            if logged_in_customer:
                if not logged_in_customer.account_active:
                    print("❌ Your account is deactivated due to overdraft limits. Please settle your balance.")
                    continue

                account = Account(logged_in_customer)
                transaction = Transaction(account)

# This code displays the current balance of the logged-in customer's checking and savings accounts.
                if action == '2':
                    print(f"📄 Checking Account Balance: ${logged_in_customer.balance_checking}")
                    print(f"📄 Savings Account Balance: ${logged_in_customer.balance_savings}")

# This code handles deposit and withdrawal actions by taking the amount as input 
# and executing the respective deposit or withdraw operation through the transaction object.

                elif action == '3':
                    amount = float(input("Enter amount to deposit: "))
                    transaction.execute('deposit', amount)
                    for i, customer in enumerate(customers):
                        if customer[0] == logged_in_customer.account_id:
                            customers[i][4] = logged_in_customer.balance_checking
                            customers[i][5] = logged_in_customer.balance_savings
                    bank_data.save_data(customers)

                elif action == '4':
                    amount = float(input("Enter amount to withdraw: "))
                    transaction.execute('withdraw', amount)
                    for i, customer in enumerate(customers):
                        if customer[0] == logged_in_customer.account_id:
                            customers[i][4] = logged_in_customer.balance_checking
                            customers[i][5] = logged_in_customer.balance_savings
                    bank_data.save_data(customers)

# This code handles money transfers, allowing the user to choose between transferring between their own accounts 
# (Checking to Savings or vice versa) or transferring money to another customer, including selecting the transfer direction and recipient.
        
                elif action == '5':
                    success = False 
                    print("Select transfer option:")
                    print("1. Transfer between your own accounts")
                    print("2. Transfer money to another customer")
                    transfer_option = input("Enter your choice (1/2): ")

                    if transfer_option == '1':
                        
                        print("Select transfer direction:")
                        print("1. Transfer from Checking to Savings")
                        print("2. Transfer from Savings to Checking")
                        transfer_direction = input("Enter your choice (1/2): ")

                        amount = float(input("Enter amount to transfer: "))

                        if transfer_direction == '1':
                            
                            if account.transfer(amount, from_checking_to_savings=True):
                                print(f"✅ ${amount} transferred from Checking to Savings.")
                                success = True
                            else:
                                print("❌ Insufficient funds! Transfer failed.")
                        elif transfer_direction == '2':
                            
                            if account.transfer(amount, from_checking_to_savings=False):
                                print(f"✅ ${amount} transferred from Savings to Checking.")
                                success = True
                            else:
                                print("❌ Insufficient funds! Transfer failed.")

                        else:
                            print("❌ Invalid choice! Please select either 1 or 2.")
                    
                    elif transfer_option == '2':
                        
                        recipient_account_id = input("Enter recipient's account ID: ")
                        
                        for customer in customers:
                            if customer[0] == recipient_account_id:  
                                recipient = Customer(*customer)
                                break

                        if recipient:
                            print("Recipient found.")
                            print("Select transfer direction:")
                            print("1. Transfer from Checking to recipient's Checking")
                            print("2. Transfer from Savings to recipient's Checking")
                            transfer_direction = input("Enter your choice (1/2): ")

                            amount = float(input("Enter amount to transfer: "))
                            if transfer_direction == '1':
                                if account.transfer_to_other_customer(amount, recipient, from_checking_to_savings=False, from_checking_to_checking=True):
                                    print(f"✅ ${amount} transferred from Checking to {recipient.first_name} {recipient.last_name}'s Checking.")
                                    success = True
                                else:
                                    print("❌ Insufficient funds! Transfer failed.")
                            elif transfer_direction == '2':
                                if account.transfer_to_other_customer(amount, recipient, from_checking_to_savings=True, from_checking_to_checking=False):
                                    print(f"✅ ${amount} transferred from Savings to {recipient.first_name} {recipient.last_name}'s Checking.")
                                    success = True
                                else:
                                    print("❌ Insufficient funds! Transfer failed.")  
                        else:
                            print("❌ Recipient not found.")

# This code handles overdraft management for the logged-in 
# customer, updates the customer data with the latest balance and account status, and saves the updated data to the bank's storage (CSV or database).

                    account.handle_overdraft()  
                    if success:
                        for i, customer in enumerate(customers):
                            if customer[0] == logged_in_customer.account_id:
                                customers[i][4] = logged_in_customer.balance_checking
                                customers[i][5] = logged_in_customer.balance_savings
                                
                            if recipient and customer[0] == recipient.account_id:
                                customers[i][4] = recipient.balance_checking
                                customers[i][5] = recipient.balance_savings
                                
                        bank_data.save_data(customers)

# This code allows the user to reactivate a deactivated account, checks if the account is active or not, 
# updates the account status, and saves the updated customer data to the storage.

                if action == '6':  
                            account_id = input("Enter your account ID: ")

                            for customer in customers:
                                if customer[0] == account_id:
                                    logged_in_customer = Customer(*customer)

                                    if logged_in_customer.account_active:
                                        print("✅ Your account is already active.")
                                    else:
                                        logged_in_customer.reactivate_account()

                                
                                        for i, cust in enumerate(customers):
                                            if cust[0] == logged_in_customer.account_id:
                                                customers[i][4] = logged_in_customer.balance_checking
                                                customers[i][6] = logged_in_customer.overdraft_count
                                                customers[i][7] = logged_in_customer.account_active

                                
                                        bank_data.save_data(customers)
                                        print("✅ Your account has been reactivated successfully.")
                                    break
                            else:
                                print("❌ Account not found.")
#  this code to exit from the program or logout 
        elif action == '7':
            print("🚪 Goodbay....Thank you for using Titan Bank! Have a great day🤩.")
            break
        else:
            print("❌ Invalid option. Please try again.")
# This line checks if the script is being run directly (not imported as a module) 
# calls the main function to execute the program's logic
if __name__ == "__main__":
    main()