# -*- coding: utf-8 -*-
"""
Created on Thursday June 1 16:23:00 2023

@author: Byron K Nelson
This Program Prompts the User to Enter the Name, Weight and Height and Creates a Dictionary
Object with the Entered Data.
  
  -Input: None
  -Output: A Dictionary Object Containing Name, Weight & Height

"""

from Homework2 import dataRecorder

def enterData():
    """
    This Creates a Dictionary of Entered Names and Weights

    -Input: None
    -Output: A Dictionary Object to Pass to dataRecorder() in Homework2.py
  
    """
    
    # Prompt User to Enter a Name
    try:
        name = input("Please Enter Your Name: ")
        # Check if Name Contains Any Special Characters Other Than Space
        if any(char.isalnum() or char.isspace() for char in name) is False:
            raise ValueError("Invalid Name Entry. Name Can Only Contain Alphanumeric Characters and Spaces!")
    except ValueError as e:
        print(str(e))
        exit(-1)
        
    # Prompt User for Weight and Height
    try:
        weight = float(input("Please Enter the Weight in Pounds: "))
        height = float(input("Please Enter the Height in Feet: "))
    except (ValueError, RuntimeError, TypeError, NameError):
        print("Invalid Entry")
        exit(-1)

    if height == 0 or weight == 0:
        print("Invalid Weight or Height!")
        exit(0)

    # Create a Dictionary Object With the User's Data
    record = {"Name": name, "Weight": weight, "Height": height}
    
    # Call the dataRecorder Function to Write the Record to a File
    dataRecorder("data.csv", record)
    
    return record
    
# Example Usage
#record = enterData()
#dataRecorder("data.csv", record)