import csv
##########################################  CLASS BANK_DATA  ###############################################

class Bank_data:
    def __init__(self,filename):
        self.filename=filename
    def load_data(self):
        customer=[]
        with open(self.filename, mode='r')as file:
            csv_reader= csv.reader(file)
            for row in csv_reader:
                customer.append(row)
        return customer
    
    def save_data(self, customer):
        with open(self.filename, mode='w', newline='') as file:
            csv_writer= csv.writer(file)
            csv_writer.writerows(customer)
##########################################  CLASS CUSTOMER  ###############################################
##########################################  CLASS BANK_ACCOUNT  ###############################################
##########################################  CLASS TRANSACTION  ###############################################
def main():
bank_data= Bank_data('bank1.csv')
customer =bank_data.load_data()
