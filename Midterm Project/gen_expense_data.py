import argparse
import os
import random
import calendar
import csv
from datetime import datetime, date
from faker import Factory

# Constants
EXPENSE_CATEGORIES = ['CCBill', 'Utility', 'Mortgage', 'Misc']
EXPENSE_NAMES = ['Chase', 'House1', 'House2', 'Water', 'Internet', 'Power', 'Amex']
PAYMENT_METHODS = ['Bank Draft']

BASE_FOLDER = "AnnualExpenseData"
CATEGORY_FILE = "expense_categories.txt"
NAME_FILE = "expense_names.txt"
PAYMENT_FILE = "payment_methods.txt"
HEADER_FIELDS = ["Year", "Month", "Expense Category", "Expense Name", "Amount Due", "Due Date", "Amount Paid", "Payment Date", "Payment Method"]

def generate_expense_data(start_year, end_year):
    """
    This method generates a folder of CSV files with fake data that holds fields of expense categories, names, due date, amount paid, etc.
    This method also generates text files of the base expense categories, names and payment methods that can be added to later.
    
    - Inputs: The Command Line Arguments That Specify the Year Range to Generate Fake Expense Data
    - Outputs: The Folder "AnnualExpenseData" With the Specified Number of Fake CSV Files in the Year
      Range, as Well as Text Files With the Base Expense Categories, Names and Payment Types
    
    """
    # Create the Folder if it Doesn't Exist
    folder_path = os.path.join(os.getcwd(), 'AnnualExpenseData')

    # Check if the Folder Exists
    folder_exists = False
    try:
        os.makedirs(folder_path, exist_ok=True)
        folder_exists = True
    except FileExistsError:
        pass
    
     # Create and Write Expense Categories to File
    category_file_path = os.path.join(folder_path, CATEGORY_FILE)
    if not os.path.exists(category_file_path):
        with open(category_file_path, 'w') as category_file:
            category_file.write('\n'.join(EXPENSE_CATEGORIES))

    # Create and Write Expense Names to File
    name_file_path = os.path.join(folder_path, NAME_FILE)
    if not os.path.exists(name_file_path):
        with open(name_file_path, 'w') as name_file:
            name_file.write('\n'.join(EXPENSE_NAMES))

    # Create and Write Payment Methods to File
    payment_file_path = os.path.join(folder_path, PAYMENT_FILE)
    if not os.path.exists(payment_file_path):
        with open(payment_file_path, 'w') as payment_file:
            payment_file.write('\n'.join(PAYMENT_METHODS))
    
    fake = Factory.create("hi_IN")  # Create an Instance of the Faker Factory

    for year in range(start_year, end_year + 1):
        file_name = f"{year}MonthlyExpenses.csv"
        file_path = os.path.join(folder_path, file_name)

        # Check if the File Exists
        file_exists = False
        try:
            with open(file_path, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass

        # Write the Records to the File
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write Header Only if the File Doesn't Exist
            if not file_exists:
                writer.writerow(HEADER_FIELDS)

            for month in range(1, 13):
                month_name = calendar.month_name[month]
                days_in_month = calendar.monthrange(year, month)[1]
                expense_data = []

                for category in EXPENSE_CATEGORIES:
                    expense_name = fake.random_element(EXPENSE_NAMES)
                    amount_due = round(fake.random.uniform(10, 500), 2)  # Generate Random Amount Due
                    due_date = fake.random_int(1, days_in_month)
                    start_date = date(year, month, 1)  # Construct Start Date as a Date Object
                    end_date = date(year, month, days_in_month)  # Construct End Date as a Date bject
                    amount_paid = round(fake.random.uniform(0, amount_due), 2)  # Generate Random Amount Paid
                    payment_date = fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
                    payment_method = fake.random_element(PAYMENT_METHODS)

                    expense_data.append([
                        year, month_name, category, expense_name, amount_due,
                        due_date, amount_paid, payment_date, payment_method
                    ])

                writer.writerows(expense_data)   

        print(f"Generated Expense Data for {month_name}, {year} in File: {file_name}")

def parse_arguments():
    """
    This method parses the argument string in the command prompt, entered by the user. It determines the year range entered by the user
    so "generate_expense_data()" knows how many fake CSV files to generate. An example of the usage of this is: 
    "python gen_expense_data.py -Year1 2018 -Year2 2023". After much research, it was decided to use the "parser" command rather than the 
    Regular Expressions that were talked about in class. This is so much easier and more efficient when you are dealing with strings.
    
    - Input: None
    - Outputs: The Parsed Argument String Entered By the User in the Command Prompt
    
    """
    parser = argparse.ArgumentParser(description='Generate Random Expense Data.')
    parser.add_argument('-Year1', dest='start_year', type=int, help='Start Year for Expense Data Generation')
    parser.add_argument('-Year2', dest='end_year', type=int, help='End Year for Expense Data Generation')
    parser.add_argument('-folder', dest='folder_name', default='AnnualExpenseData',
                        help='Subfolder Name to Store the Expense Files')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    generate_expense_data(args.start_year, args.end_year)