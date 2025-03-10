import csv
##########################################  CLASS BANK_DATA  ###############################################

class Bank_data:
    def __init__(self,filename):
        self.filename=filename
    def load_data(self):
        customers=[]
        with open(self.filename, mode='r')as file:
            csv_reader= csv.reader(file)
            for row in csv_reader:
                customers.append(row)
        return customers
    
    def save_data(self, customers, append=False):
        mode = 'a' if append else 'w'
        with open(self.filename, mode=mode, newline='') as file:
            csv_writer = csv.writer(file)
            if append:
               csv_writer.writerow(customers[-1])
            else:
                csv_writer.writerows(customers)
##########################################  CLASS CUSTOMER  ###############################################
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
class Account:
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

    def transfer(self, amount):
        if self.customer.balance_checking >= amount:
            self.customer.balance_checking -= amount
            self.customer.balance_savings += amount
            return True
        return False

    def handle_overdraft(self):
        if self.customer.balance_checking < 0:
            self.customer.overdraft_count += 1
            self.customer.apply_overdraft_fee()
            if self.customer.overdraft_count >= 2:
                self.customer.deactivate_account() 

##########################################  CLASS TRANSACTION  ###############################################

######## MAINE FUNCTION TO Handles user banking operations
def main():
    bank_data = Bank_data('bank1.csv')
    customers = bank_data.load_data()

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
                bank_data.save_data(customers, append=True)
                print(f"✅ New account for {new_customer.first_name} {new_customer.last_name} has been added.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid number for balance.")

        elif action in ['2', '3', '4', '5', '6']:
            if not logged_in_customer:
                account_id = input("Enter account ID: ").strip()
                password = input("Enter password: ").strip()

                for customer in customers:
                    if len(customer) < 8:  
                        continue
                    stored_account_id = customer[0].strip()  
                    stored_password = customer[3].strip()    
                    if customer[0] == account_id:
                        logged_in_customer = Customer(*customer)
                        if not logged_in_customer.check_password(password):
                            print("❌ Incorrect password!")
                            logged_in_customer = None
                            break
                        else:
                            print(f"✅ Welcome {logged_in_customer.first_name} {logged_in_customer.last_name}!")
                            break

                if not logged_in_customer:
                    print("❌ Account not found or incorrect password.")
                    continue

            if logged_in_customer:
                if not logged_in_customer.account_active:
                    print("❌ Your account is deactivated due to overdraft limits. Please settle your balance.")
                    continue
                account = Account(logged_in_customer)

                if action == '2':
                    print(f"📄 Checking Account Balance: ${logged_in_customer.balance_checking}")
                    print(f"📄 Savings Account Balance: ${logged_in_customer.balance_savings}")

                elif action == '3':
                    amount = float(input("Enter amount to deposit: "))
                    transaction.execute('deposit', amount)

                elif action == '4':
                    amount = float(input("Enter amount to withdraw: "))
                    transaction.execute('withdraw', amount)

                elif action == '5':
                    amount = float(input("Enter amount to transfer: "))
                    transaction.execute('transfer', amount)

                account.handle_overdraft()

                # تحديث البيانات في القائمة
                for i, customer in enumerate(customers):
                    if customer[0] == logged_in_customer.account_id:
                        customers[i][4] = logged_in_customer.balance_checking
                        customers[i][5] = logged_in_customer.balance_savings
                        customers[i][6] = logged_in_customer.overdraft_count
                        customers[i][7] = logged_in_customer.account_active
                bank_data.save_data(customers)

                if action == '6':  # ✅ تصحيح إعادة تنشيط الحساب
                    account_id = input("Enter your account ID: ")

                    for customer in customers:
                        if customer[0] == account_id:
                            logged_in_customer = Customer(*customer)

                            if logged_in_customer.account_active:
                                print("✅ Your account is already active.")
                            else:
                                logged_in_customer.reactivate_account()

                        # تحديث البيانات في القائمة
                                for i, cust in enumerate(customers):
                                    if cust[0] == logged_in_customer.account_id:
                                        customers[i][4] = logged_in_customer.balance_checking
                                        customers[i][6] = logged_in_customer.overdraft_count
                                        customers[i][7] = logged_in_customer.account_active

                        # حفظ البيانات المحدثة في الملف
                                bank_data.save_data(customers)
                                print("✅ Your account has been reactivated successfully.")
                            break
                    else:
                        print("❌ Account not found.")

        if action == '7':
            print("🚪 Exiting the program.")
            break  # Make sure to break the loop here

        else:
           print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
