#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 2023

This program is multi-faceted. First there is a file, "gen_expense_data.py" that generates false data that tracks monthly expenses for years specified in a 
range by the user. The files created are CSV files. Text files are also created that hold the categories, names and payment methods of expenses in a personal 
budget. All files are intended to be able to be edited by this program. Add an expense, modify an expense, import an outside expense CSV, and also be able to 
analyze all of the data and create reports and graphs according to the user's preference.

@author: Byron K. Nelson
"""

import os
import sys
import csv
import shutil
import calendar
import matplotlib.pyplot as plot
import datetime

# Constants
EXPENSE_CATEGORIES = []
EXPENSE_NAMES = []
PAYMENT_METHODS = []

BASE_FOLDER = "AnnualExpenseData"
CATEGORY_FILE = "expense_categories.txt"
NAME_FILE = "expense_names.txt"
PAYMENT_FILE = "payment_methods.txt"
HEADER_FIELDS = ["Year", "Month", "Expense Category", "Expense Name", "Amount Due", "Due Date", "Amount Paid", "Payment Date", "Payment Method"]

# Construct the File Paths
folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
category_file_path = os.path.join(folder_path, CATEGORY_FILE)
name_file_path = os.path.join(folder_path, NAME_FILE)
payment_file_path = os.path.join(folder_path, PAYMENT_FILE)

# Function to Load Expense Categories from File
def load_expense_categories():
    """
    This method loads the text file created in "gen_expense_data.py" that has the available categories: 
    "expense_categories.txt"
    
    This method is loaded in main() at the beginning of the program
    
    - Input: None
    - Output: None
    
    """
    if os.path.isfile(category_file_path):  # Check if File Exists Already
        with open(category_file_path, "r") as file:
            for line in file:
                category = line.strip()
                EXPENSE_CATEGORIES.append(category)

# Function to Load Expense Names from File
def load_expense_names():
    """
    This method loads the text file created in "gen_expense_data.py" that has the available categories: 
    "expense_names.txt"
    
    This method is loaded in main() at the beginning of the program
    
    - Input: None
    - Output: None
    
    """
    if os.path.isfile(name_file_path):  # Check if File Exists Already
        with open(name_file_path, "r") as file:
            for line in file:
                name = line.strip()
                EXPENSE_NAMES.append(name)
                
# Function to Load Payment Methods from File
def load_payment_methods():
    """
    This method loads the text file created in "gen_expense_data.py" that has the available categories: 
    "payment_methods.txt"
    
    This method is loaded in main() at the beginning of the program
    
    - Input: None
    - Output: None
    
    """
    if os.path.isfile(payment_file_path):  # Check if File Exists Already
        with open(payment_file_path, "r") as file:
            for line in file:
                method = line.strip()
                PAYMENT_METHODS.append(method)

# Function to Add a New Expense
def add_new_expense():
    """
    This method accomplishes part a) of Task 2, which is to add a new expense to one of the existing randomly generated
    CSV files. It appends the new expense record to the end of the file.
    
    This method is called in main() if the user chooses option a) in the main menu displayed
    
    - Input: None
    - Output: The Added Expense Record to the Corresponding CSV File
    
    """
    print("\nAdd a New Expense")
    print("------------------")
    
    # Get User Input for Expense Details
    category = input("Expense Category: ")
    while not is_valid_category(category):
        print("Invalid Category. Available Categories:", EXPENSE_CATEGORIES)
        category = input("Expense Category: ")
        
    name = input("Expense Name: ")
    while not is_valid_name(name):
        print("Invalid Name. Available Names:", EXPENSE_NAMES)
        name = input("Expense Name: ")
        
    amount_due = input("Amount Due: ")
    while not is_valid_amount(amount_due):
        print("Invalid Amount Format. Please Enter a Valid Amount.")
        amount_due = input("Amount Due: ")
        
    day = None  # Initialize Day Variable
        
    due_date = input("Due Date (YYYY-MM-DD): ")
    while not is_valid_date(due_date):
        print("Invalid Date Format. Please Enter a Valid Date (YYYY-MM-DD).")
        due_date = input("Due Date (YYYY-MM-DD): ")
        day = int(due_date.split('-')[2])
        
    amount_paid = input("Amount Paid: ")
    while not is_valid_amount(amount_paid):
        print("Invalid Amount Format. Please Enter a Valid Amount.")
        amount_paid = input("Amount Paid: ")
        
    payment_date = input("Payment Date (YYYY-MM-DD, Optional): ")
    while payment_date and not is_valid_date(payment_date):
        print("Invalid Date Format. Please Enter a Valid Date (YYYY-MM-DD) or Leave it Empty.")
        payment_date = input("Payment Date (YYYY-MM-DD, Optional): ")
        
    payment_method = input("Payment Method: ")
    
    # Create the Expense Record
    record = [
        datetime.datetime.now().strftime('%Y'),  # Year
        datetime.datetime.now().strftime('%B'),  # Month
        category,
        name,
        amount_due,
        day,
        amount_paid,
        payment_date,
        payment_method
    ]
    
    # Write the Record to the Expense File
    folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
    file_name = f"{datetime.datetime.now().year}MonthlyExpenses.csv"
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(record)
    
    print("\nExpense Added Successfully!")

# Function to Search and Modify an Expense
def search_expense():
    """
    This method accomplishes part b) of Task 2, which is to search for and modify one of the existing randomly generated
    CSV files. It appends the modified record to the end of the file. It does NOT put the record back in the same spot.
    
    This method is called in main() if the user chooses option b) in the main menu displayed
    
    - Input: None
    - Output: The Modified Expense Record in the Corresponding CSV File
    
    """
    print("\nSearch/Modify an Expense")
    print("------------------------")
    
    # Prompt the User to Enter the Search Criteria
    year = input("Enter the Year: ")
    month = input("Enter the Month: ")
    expense_category = input("Enter the Expense Category: ")
    
    folder_path = os.path.join(os.getcwd(), BASE_FOLDER)  
    matching_records = []
    
    # Search Through CSV Files in the Folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                records = list(reader)
                for i, record in enumerate(records):
                    if (
                        record.get('Year', '').strip().lower() == year.strip().lower()
                        and record.get('Month', '').strip().lower() == month.strip().lower()
                        and record.get('Expense Category', '').strip().lower() == expense_category.strip().lower()
                    ):
                        matching_records.append((filename, i, record))
    
    # Print the Matching Expense Records
    if len(matching_records) == 0:
        print("\nNo Matching Expense Records Found!")
        return
    
    print("\nMatching Expense Records:")
    for index, record_data in enumerate(matching_records):
        filename, record_index, record = record_data
        print(f"Index: {index}, File: {filename}, Expense: {record}")
    
    if len(matching_records) > 10:
        print_records = input("\nMore Than 10 Matching Expense Entries. Print All? (y/n): ")
        if print_records.lower() != "y":
            return
    
    # Ask the User to Select a Record for Modification
    while True:
        choice = input("\nEnter the Index Number of the Record to Modify (Or Enter 'Main' to Go Back to the Main Menu): ")
        if choice.lower() == "main":
            return
        try:
            index = int(choice)
            if 0 <= index < len(matching_records):
                break
            else:
                print("\nInvalid Index Number!")
        except ValueError:
            print("\nInvalid Index Number!")
    
    _, _, record = matching_records[index]
    print("\nExpense Fields:")
    for i, field in enumerate(HEADER_FIELDS):
        print(f"{i+1}. {field}")
    
    # Prompt the User to Select a Field for Modification
    while True:
        field_choice = input("\nEnter the Number of the Field to Modify: ")
        if field_choice.isdigit() and 1 <= int(field_choice) <= len(HEADER_FIELDS):
            break
        else:
            print("\nInvalid Field Number!")
    
    field_choice = int(field_choice)
    field_name = HEADER_FIELDS[field_choice - 1]
    new_value = input(f"Enter the New Value For {field_name}: ")
    
    # Modify the Specific Field
    record[field_name] = new_value

    # Append the Modified Record to the CSV file => I Spent Days, and Days, and Days Trying to Get it To Put the Modified Record Back 
    # In Its Original Spot in the CSV. Finally, with a Day Left, I Decided to Just Try and Be Happy With Appending It. I Don't Like It.
    with open(os.path.join(folder_path, matching_records[index][0]), "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADER_FIELDS, delimiter=",")
        writer.writerow(record)
            
    print("\nRecord Modified Successfully!")
        
# Function to Add an Expense Category, Expense Name, or Payment Method
def add_expense_type():
    """
    This method accomplishes part c) of Task 2, which is to add an expense category, name or payment type to one of the corresponding
    text files created in "gen_expense_data.py". It appends the new value to the end of the corresponding empty lists. These lists are
    then sent to helper function to save them to the actual text files.
    
    This method is called in main() if the user chooses option c) in the main menu displayed
    
    - Input: None
    - Output: The Added Expense Category, Name or Payment Method to the Corresponding Text File
    
    """
    print("\nAdd an Expense Category/Expense Name/Payment Method")
    print("---------------------------------------------------")

    # Print the Current Expense Types and Payment Methods
    print("Current Expense Categories:")
    print(EXPENSE_CATEGORIES)

    print("\nCurrent Expense Names:")
    print(EXPENSE_NAMES)

    print("\nCurrent Payment Methods:")
    print(PAYMENT_METHODS)

    # Ask the User What They Want to Add
    option = input("\nWhat Do You Want to Add? (Category/Name/Method): ")

    if option.lower() == "category":
        new_category = input("Enter the New Expense Category: ")
        EXPENSE_CATEGORIES.append(new_category)
        save_expense_categories()  # Call a Function to Save the Expense Categories to a Separate File
        print("\nExpense Category Added Successfully!")

    elif option.lower() == "name":
        new_name = input("Enter the New Expense Name: ")
        EXPENSE_NAMES.append(new_name)
        save_expense_names()  # Call a Function to Save the Expense Names to a Separate File
        print("\nExpense Name Added Successfully!")

    elif option.lower() == "method":
        new_method = input("Enter the New Payment Method: ")
        PAYMENT_METHODS.append(new_method)
        save_payment_methods()  # Call a Function to Save the Payment Methods to a Separate File
        print("\nPayment Method Added Successfully!")

    else:
        print("\nInvalid Option!")

# Function to Save Expense Categories to a Separate File
def save_expense_categories():
    """
    This method saves the current expense categories in the text file "expense_categories.txt". It accesses
    the current corresponding list that was filled in add_expense_type() => "EXPENSE_CATEGORIES"
    
    - Input: None
    - Output: The New Expense Category in the Corresponding Text File
    """
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), BASE_FOLDER)
    file_path = os.path.join(folder_path, CATEGORY_FILE)
    
    with open(file_path, "w") as file:
        for category in EXPENSE_CATEGORIES:
            file.write(category + "\n")

# Function to Save Expense Names to a Separate File
def save_expense_names():
    """
    This method saves the current expense names in the text file "expense_names.txt". It accesses
    the current corresponding list that was filled in add_expense_type() => "EXPENSE_NAMES"
    
    - Input: None
    - Output: The New Expense Name in the Corresponding Text File
    
    """
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), BASE_FOLDER)
    file_path = os.path.join(folder_path, NAME_FILE)
    
    with open(file_path, "w") as file:
        for name in EXPENSE_NAMES:
            file.write(name + "\n")

# Function to Save Payment Methods to a Separate File
def save_payment_methods():
    """
    This method saves the current payment methods in the text file "payment_methods.txt". It accesses
    the current corresponding list that was filled in add_expense_type() => "PAYMENT_METHODS"
    
    - Input: None
    - Output: The New Payment Method in the Corresponding Text File
    
    """
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), BASE_FOLDER)
    file_path = os.path.join(folder_path, PAYMENT_FILE)
    
    with open(file_path, "w") as file:
        for method in PAYMENT_METHODS:
            file.write(method + "\n")

# Function to Check if an Entered Value is in the List of Available Categories
def is_valid_category(value):
    """
    This method simply returns the value if found in the list that was filled in add_expense_type() =>
    "EXPENSE_CATEGORIES"
    
    - Input: The Value Entered By the User for Expense Category
    - Output: Boolean Value of True if Valid
    
    """
    return value in EXPENSE_CATEGORIES

# Function to Check if an Entered Value is in the List of Available Names
def is_valid_name(value):
    """
    This method simply returns the value if found in the list that was filled in add_expense_type() =>
    "EXPENSE_NAMES"
    
    - Input: The Value Entered By the User for Expense Name
    - Output: Boolean Value of True if Valid
    
    """
    return value in EXPENSE_NAMES

# Function to Check if a String Represents a Valid Amount (Numeric)
def is_valid_amount(value):
    """
    This method simply returns a Boolean of "True" if the amount entered by the user for Dollars is 
    indeed a float precision number.
    
    - Input: The Value Entered By the User for Dollar Amount
    - Output: Boolean Value of True if Valid
    
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function to Check if a String Represents a Valid Date (YYYY-MM-DD)
def is_valid_date(value):
    """
    This method simply returns a Boolean of "True" if the value entered by the user for date is
    in fact in the specified date format.
    
    - Input: The Value Entered By the User for the Date
    - Output: Boolean Value of True if Valid
    
    """
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False
        
# Function to Check if a String Represents a Valid Year (YYYY)
def is_valid_year(value):
    """
    This method simply returns a Boolean of "True" if the value entered by the user for year is
    in fact in the specified year format. For Example, 1,000,000,000 would not be a valid year.
    It should be a four digit number of a real year.
    
    - Input: The Value Entered By the User for Year
    - Output: Boolean Value of True if Valid
    
    """
    try:
        datetime.datetime.strptime(value, '%Y')
        return True
    except ValueError:
        return False
        
def is_valid_month(value):
    """
    This method simply returns a Boolean of "True" if the value entered by the user for month is
    in fact in the specified month format. For Example, 25 would not be a valid month.
    It should be a two digit number of a real month.
    
    - Input: The Value Entered By the User for Month
    - Output: Boolean Value of True if Valid
    
    """
    try:
        month = int(value)
        return 1 <= month <= 12
    except ValueError:
        return False
        
def validate_integer_input(prompt):
    """
    This method simply returns a Boolean of "True" if the amount entered by the user for Year is 
    indeed an integer number. For Example, 1983.5 would not be a valid year.
    
    - Input: The Value Entered By the User for Dollar Amount
    - Output: Boolean Value of True if Valid
    
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid Input! Please Enter an Integer!")
            
class Expense:
    """
    This is a simple class declaration for an expense record that is used in import_expense_data() to categorize and label
    the expense record read from an outside file path.
    
    """
    def __init__(self, year, month, category, name, amount_due, due_date, amount_paid, payment_date, payment_method):
        self.year = year
        self.month = month
        self.category = category
        self.name = name
        self.amount_due = amount_due
        self.due_date = due_date
        self.amount_paid = amount_paid
        self.payment_date = payment_date
        self.payment_method = payment_method

def import_expense_data():
    """
    This method accomplishes part d) of Task 2, which is to allow the user to enter a different file path to search for an existing
    CSV file. It is assumed that the existing CSV file is in the exact same format as the ones generated in "gen_expense_data.py".
    
    This method is called in main() if the user chooses option d) in the main menu displayed
    
    - Input: None
    - Output: None
    
    """
    print("\nImport Expense Data")
    print("-------------------")
    
    file_path = input("\nEnter the File Path of the CSV or Text File: ")
    
    if not os.path.isfile(file_path):
        print("\nFile not found!")
        return []
    
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        expenses = []

        for row in reader:
            year = row[0]
            month = row[1]
            category = row[2]
            name = row[3]
            amount_due = row[4]
            due_date = row[5]
            amount_paid = row[6]
            payment_date = row[7]
            payment_method = row[8]

            expense = Expense(year, month, category, name, amount_due, due_date, amount_paid, payment_date, payment_method)
            expenses.append(expense)

        if len(expenses) == 0:
            print("\nNo Expense Records Found in the File!")
        else:
            print("\nImported {} Expense Records Successfully!".format(len(expenses)))

    return expenses
        
def calculate_total_expenses(year, expense_category):
    """
    This method calculates the total expenses. It is a helper function to calculate_total_annual_expenses(), which is called 
    to handle the generation of the first report for Task 3.
    
    - Inputs: The Year Entered By the User and the Expense Category Entered By the User
    - Output: The Total Annual Expenses for a Particular Expense Category or Expense Type for a Year
    
    """
    total_expenses = 0

    # Construct the File Path for the CSV 
    folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
    file_name = f"{year}MonthlyExpenses.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the File Exists
    if not os.path.isfile(file_path):
        print(f"No Expense Data Found for the Year {year}")
        return total_expenses

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if the Expense Category Matches
                if row[2] == expense_category:
                    amount = float(row[4])
                    total_expenses += amount
    except Exception as e:
        print(f"An Error Occurred While Calculating Expenses: {str(e)}")

    return total_expenses

def calculate_total_annual_expenses(start_year, end_year, expense_category):
    """
    This method calculates the total annual expenses. It is called to handle the generation of the first report for Task 3.
    It calculates the total annual expenses in a particular category for an entire year, but in the range specified by the user.
    
    - Inputs: The Start Year Entered By the User, The End Year Entered By the User and the Expense Category Entered By the User
    - Output: The Total Annual Expenses for a Particular Expense Category or Expense Type for a Range of Years
    
    """
    report_data = []

    for year in range(start_year, end_year + 1):
        total_expense = calculate_total_expenses(year, expense_category)
        annual_expense = (year, total_expense)  # Create a tuple (year, total_expense)
        report_data.append(annual_expense)

    return report_data
    
def calculate_expenses_by_year_range(expense_type, start_year, end_year):
    """
    This method calculates the total annual expenses. It is called to handle the generation of the second report for Task 3, and the 
    second graph for Task 4. It calculates the total annual expenses in a particular category for an entire year, but in the range 
    specified by the user, more in a histogram-style format.
    
    - Inputs:  The Expense Category Entered By the User, The Start Year Entered By the User & The End Year Entered By the User
    - Output: Expenses for an Expense Type or Category for a Year Range or a Particular Year in Sub Bar Graph Form
    
    """
    report_data = []

    for year in range(start_year, end_year + 1):
        total_expense = 0.0
        expense_category = ""  

        # Construct the File Path for the CSV 
        folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
        file_name = f"{year}MonthlyExpenses.csv"
        file_path = os.path.join(folder_path, file_name)

        # Check if the File Exists
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        # Check if the Expense Type Matches
                        if row[2].lower() == expense_type.lower():
                            amount = float(row[4])
                            total_expense += amount
                            # Get the Expense Category from the CSV file
                            expense_category = row[3]
            except Exception as e:
                print(f"\nAn Error Occurred While Calculating Expenses: {str(e)}")
        else:
            print(f"\nNo Expense Data Found for the Year {year}")

        report_data.append(total_expense)

    return report_data
    
def calculate_monthly_expenses(year):
    """
    This method calculates the total monthly expenses of every type. It is called to handle the generation of the third report for Task 3, and the 
    fourth graph for Task 4. It calculates the total monthly expenses in every category for an entire year, but in the range specified by the user.
    
    - Input:  The Specific Year That's in the Range Specified By the User
    - Output: Monthly Expenses in a Particular Year
    
    """
    report_data = [("Month", "Total Monthly Expenses")]

    # Construct the File Path for the CSV 
    folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
    file_name = f"{year}MonthlyExpenses.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the File Exists
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the Header Row
                
                total_expenses = [0.0] * 13  
                month_names = []
                
                for row in reader:
                    month_name = row[1]
                    month = list(calendar.month_name).index(month_name)
                    amount = float(row[4])

                    # Check if the Month and Year Match
                    if int(row[0]) == year:
                        total_expenses[month] += amount
                        month_names.append(month_name)
                        
                for month in range(1, 13):
                    month_name = calendar.month_name[month]
                    report_data.append((month_name, total_expenses[month]))
                        
        except Exception as e:
            print(f"\nAn Error Occurred While Calculating Expenses: {str(e)}")
    else:
        print(f"\nNo Expense Data Found for the Year {year}")

    return report_data

def calculate_expenses_by_category_for_year(year):
    """
    This method calculates the total monthly expenses of every type. It is called to handle the generation of the third report for Task 3, and the 
    fourth graph for Task 4. It calculates the total monthly expenses in every category for an entire year, but in the range specified by the user.
    
    - Input:  The Specific Year That's in the Range Specified By the User
    - Output: Monthly Expenses in a Particular Year
    
    """
    expense_categories = []
    total_expenses = []

    # Construct the File Path for the CSV
    folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
    file_name = f"{year}MonthlyExpenses.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the File Exists
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the Header Row
                expenses_by_category = {}

                for row in reader:
                    expense_category = row[2]
                    amount = float(row[4])

                    if expense_category in expenses_by_category:
                        expenses_by_category[expense_category] += amount
                    else:
                        expenses_by_category[expense_category] = amount

                for category, total_expense in expenses_by_category.items():
                    expense_categories.append(category)
                    total_expenses.append(total_expense)
                    
        except Exception as e:
            print(f"\nAn Error Occurred While Calculating Expenses: {str(e)}")
    else:
        print(f"\nNo Expense Data Found for the Year {year}")

    return expense_categories, total_expenses

# Function to Generate Reports
def generate_report():
    """
    This method accomplishes Task 3, which is to generate 3 different reports, chosen by the user, of analysis of the CSV files.
    A user menu is displayed showing the three types of reports that will be generated.
    
    This method is called in the command prompt if the argument "--report" is given right after the command to run the program:
    "python manageExpenses.py --report"
    
    - Input: None
    - Output: The Corresponding Report as a CSV File Chosen by the User
    
    """
    print("\nGenerate Reports")
    print("----------------\n")
    
    # User Menu for Report Types
    print("Select a Report Type:")
    print("\n1. Total Annual Expenses for a Particular Expense Category or Expense Type for a Range of Years.")
    print("2. Expenses for an Expense Type or Category for a Year Range or a Particular Year.")
    print("3. Monthly Expenses in a Particular Year.\n")

    # Get Report Type from the User
    report_type = input("Enter Report Type (1-3): ")

    if report_type == "1":
        report_filename = input("Enter Report Filename: ")
        expense_category = input("Enter Expense Category: ")
        start_year = int(input("Enter Start Year: "))
        end_year = int(input("Enter End Year: "))  
        
        # Append .csv Extension if Not Already Present
        if not report_filename.endswith(".csv"):
            report_filename += ".csv"

        # Calculate the Total Annual Expenses for the Given Expense Category and Year Range
        report_data = calculate_total_annual_expenses(start_year, end_year, expense_category)

        # Generate the Report File With the Specified Columns and Data
        report_folder = os.path.join(os.getcwd(), "expensereports")

        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
            print(f"\nReport Folder '{report_folder}' Created Successfully!")

        report_file = os.path.join(report_folder, report_filename)

        # Generate the Report File With the Specified Columns and Data
        with open(report_file, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
    
            # Write the Header Row
            writer.writerow(["Expense Type", "", "Year", "Expense"])
    
            # Write the Data Rows
            for year, total_expense in report_data:
                writer.writerow([expense_category, "", year, total_expense])  # Write year and total_expense Separately

        print(f"\nReport File '{report_filename}' Generated Successfully in '{report_folder}'.")

    elif report_type == "2":
        report_filename = input("Enter Report Filename: ")
        expense_type = input("Enter Expense Type: ")
        start_year = int(input("Enter Start Year: "))
        end_year = int(input("Enter End Year: "))
        
        # Append .csv Extension if Not Already Present
        if not report_filename.endswith(".csv"):
            report_filename += ".csv"
    
        expenses = calculate_expenses_by_year_range(expense_type, start_year, end_year)
        report_data = [("Expense Type", "Year", "Expense")]
     
        for year, expense in zip(range(start_year, end_year + 1), expenses):
            report_data.append((expense_type, year, expense))
    
        report_folder = os.path.join(os.getcwd(), "expensereports")

        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
            print(f"\nReport Folder '{report_folder}' Created Successfully!")

        report_file = os.path.join(report_folder, report_filename)

        with open(report_file, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(report_data)

        print(f"\nReport File '{report_filename}' Generated Successfully in '{report_folder}'.")

    elif report_type == "3": 
        report_filename = input("Enter Report Filename: ")
        year = int(input("Enter Year: "))
        
        # Append .csv Extension if Not Already Present
        if not report_filename.endswith(".csv"):
            report_filename += ".csv"
        
        # Calculate the Monthly Expenses for the Given Year
        report_data = calculate_monthly_expenses(year)

        # Generate the Report File With the Specified Columns and Data
        report_folder = os.path.join(os.getcwd(), "expensereports")

        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
            print(f"\nReport Folder '{report_folder}' Created Successfully!")

        report_file = os.path.join(report_folder, report_filename)

        with open(report_file, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(report_data)

        print(f"\nReport File '{report_filename}' Generated Successfully in '{report_folder}'.")
    else:
        print("\nInvalid Report Type! Please Enter a Valid Report Type Number (1-3).")
        
def save_or_show_plot():
    """
    This method calculates the total monthly expenses of every type. It is called to handle the generation of the third report for Task 3, and the 
    fourth graph for Task 4. It calculates the total monthly expenses in every category for an entire year, but in the range specified by the user.
    
    - Input:  None
    - Output: A Display of a Graph, Either as a Spyder Window, or a Saved Image File
    
    """
    print("\nHow Would You Like to View the Graph?")
    print("\n1. Show the Graph in Spyder")
    print("2. Save the Graph as an Image File")
    
    choice = input("\nEnter Your Choice (1-2): ")
    
    if choice == "1":
        plot.show()
    elif choice == "2":
        folder_path = os.path.join(os.getcwd(), BASE_FOLDER)
        os.makedirs(folder_path, exist_ok=True)  # Create the subfolder if it doesn't exist
        
        file_name = input("Enter the Image File Name (e.g., graph): ")
        file_name += ".png"  # Append ".png" Extension
        
        file_path = os.path.join(folder_path, file_name)  
        
        plot.savefig(file_path)
        print(f"\nGraph Saved as {file_path}")
    else:
        print("\nInvalid Choice! The Graph Will Be Shown in Spyder.")
        plot.show()

def generate_graphs():
    """
    This method accomplishes Task 4, which is to generate 4 different graphs, chosen by the user, of analysis of the CSV files.
    A user menu is displayed showing the four types of graphs that will be generated. I chose to add a user menu with two 
    options for viewing the graphs. If the user has Spyder, and chooses option 1, then a Spyder Window will pop up that has the
    graph on display. If they don't have Spyder, and still want to view the graph, they can choose to save the graph as an image
    file that will be located in the "AnnualExpenseData" folder.
    
    This method is called in the command prompt if the argument "--graph" is given right after the command to run the program:
    "python manageExpenses.py --graph"
    
    - Input: None
    - Output: The Corresponding Graph, Either in a Spyder Window, or Saved as an Image File, Chosen by the User
    
    """
    print("\nGenerate Graphs")
    print("----------------\n")
    
    # User Menu for Graph Types
    print("Select a Graph Type:")
    print("\n1. Bar Graph of Total Annual Expenses for a Particular Expense Type or Category for a Range of Years.")
    print("2. Bar Graph with Sub Bars Representing Each Expense Type/Category for a Year Range.")
    print("3. Pie Chart of Expenses in Each Expense Type or Category for a Given Year.")
    print("4. Bar Graph of Total Monthly Expenses for a Given Year.")
    
    # Get Graph Type from the User
    graph_type = input("\nEnter Graph Type (1-4): ")
    
    if graph_type == "1":
        # Bar Graph of Total Annual Expenses for a Particular Expense Type or Category for a Range of Years
        expense_category = input("Enter Expense Category: ")
        
        # Validate the Expense_Category Input
        while not is_valid_category(expense_category):
            print("Invalid Expense Category! Please Enter a Valid Category.")
            expense_category = input("Enter Expense Category: ")
        
        start_year = validate_integer_input("Enter Start Year: ")
        end_year = validate_integer_input("Enter End Year: ")
        
        years = list(range(start_year, end_year + 1))
        expenses = calculate_total_annual_expenses(start_year, end_year, expense_category)
        
        # Extract the Total Expense Values From the List of Tuples
        expense_values = [total_expense for year, total_expense in expenses]
        
        plot.bar(years, expense_values) 
        plot.xlabel("Year")
        plot.ylabel("Total Expense")
        plot.title(f"Total Annual Expenses for {expense_category} ({start_year}-{end_year})") 
        save_or_show_plot()
        
    elif graph_type == "2":
        # Bar Graph with Sub Bars Representing Each Expense Type/Category for a Year Range
        start_year = validate_integer_input("Enter Start Year: ")
        end_year = validate_integer_input("Enter End Year: ")
    
        expense_types = EXPENSE_CATEGORIES  # List of Expense Types/Categories
    
        # Validate the Start_Year and End_Year Inputs
        while not (1980 <= start_year <= 2022) or not (1980 <= end_year <= 2022) or end_year < start_year:
            print("\nInvalid Year Range! Please Enter Valid Start and End Years.\n")
            start_year = validate_integer_input("Enter Start Year: ")
            end_year = validate_integer_input("Enter End Year: ")
    
        years = range(start_year, end_year + 1)
    
        num_expense_types = len(expense_types)
        bar_width = 0.8 / num_expense_types
    
        fig, ax = plot.subplots()
    
        for i, expense_type in enumerate(expense_types):
            expenses = list(calculate_expenses_by_year_range(expense_type, start_year, end_year))
        
            x = [year + i * bar_width for year in years]
            ax.bar(list(x), list(expenses), width=bar_width, label=expense_type)
        
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Expense")
        ax.set_title(f"Total Expenses by Expense Type/Category ({start_year}-{end_year})")
        ax.legend()
        save_or_show_plot()
 
    elif graph_type == "3":
        # Pie Chart of Expenses in Each Expense Type or Category for a Given Year
        year = validate_integer_input("Enter Year: ")
    
        # Validate the Year Input
        while not (1980 <= year <= 2022):
            print("\nInvalid Year! Please Enter a Valid Year!")
            year = validate_integer_input("Enter Year: ")
    
        expense_categories, total_expenses = calculate_expenses_by_category_for_year(year)
    
        plot.pie(total_expenses, labels=expense_categories, autopct="%1.1f%%")
        plot.title(f"Expenses by Expense Type/Category ({year})")
        save_or_show_plot()
        
    elif graph_type == "4":
        # Bar Graph of Total Monthly Expenses for a Given Year
        year = validate_integer_input("Enter Year: ")
    
        # Validate the Year Input
        while not (1980 <= year <= 2022):
            print("\nInvalid year! Please Enter a Valid Year!")
            year = validate_integer_input("Enter Year: ")
    
        report_data = calculate_monthly_expenses(year)
        
        months = [data[0] for data in report_data[1:]]
        expenses = [data[1] for data in report_data[1:]]
    
        plot.bar(months, expenses)
        plot.xlabel("Month")
        plot.ylabel("Total Expense")
        plot.title(f"Total Monthly Expenses ({year})")
        save_or_show_plot()

    else:
        print("\nInvalid Graph Type! Please Enter a Valid Graph Type!")

# Function That Prints the Main Menu of the Program
def print_menu():
    """
    This method simply displays the main user menu of the program.
    
    - Input:  None
    - Output: The Main Menu for the User to Decide Which Operation to Choose
    
    """
    print("\nExpense Tracking Application")
    print("----------------------------")
    print("\na) Add a New Expense")
    print("b) Search/Modify an Expense")
    print("c) Add an Expense Category or Expense Name")
    print("d) Import Expense Data")
    print("e) Close the Program\n")

def get_user_choice():
    """
    This method simply determines whether or not the user's choice is in the available choice options.
    
    - Input:  None
    - Output: The Letter of The User-Chosen Option in the Main Menu
    
    """
    valid_choices = ['a', 'b', 'c', 'd', 'e']
    
    while True:
        choice = input("Enter Your Choice (A-E): ").lower()
        if choice in valid_choices:
            return choice
        else:
            print("Invalid Choice! Please Enter a Valid Option (A-E).")
            
# Main Program
def main():
    """
    This is the main driver function of the program. Its job is to load the saved text files created in "gen_expense_data.py" that track
    the different expense categories, names and payment methods. It then runs a loop that allows the main menu to be displayed to the user
    and determine which choice they pick, which correpsonding function to call. It also allows the function calls of the command line
    arguments.
    
    """
    # Call the Functions to Load Initial Data
    load_expense_categories()
    load_expense_names()
    load_payment_methods()
    
    # Generate a Report of User Operations
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_report()
    
    # Generate Graphs of User Operations
    elif len(sys.argv) > 1 and sys.argv[1] == "--graph":
        generate_graphs()
    
    else:
        while True:
            print_menu()
            choice = get_user_choice()
            
            # User Menu Display
            if choice == 'a':
                add_new_expense() # Add a New Expense to the CSV File
            elif choice == 'b':
                search_expense()  # Search/Modify an Expense
            elif choice == 'c':
                add_expense_type() # Add New Element(s) to Expense Type List
            elif choice == 'd':
                import_expense_data()  # Call the Import of Outside Expense Data
            elif choice == 'e':
                print("\nClosing the Program...")
                break

if __name__ == '__main__':
    main()