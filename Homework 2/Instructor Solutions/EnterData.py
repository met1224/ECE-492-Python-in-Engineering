"""#
#Created on Friday May 28 2022

# @author: Justin Kaylor
# This is a program to collect user input of {name: , weight: , height:}
# and call function datarecorder so it can write or append that to a csv file
#"""
from Homework2 import dataRecorder    #import in proper function from homework2
import os
import csv

filename = "healthData.csv"
User_record = []

while True:
    try:
        name = str(input("Please enter your name: "))
        if name.replace(' ', '').isalpha() != True:
            print('Please enter only letters or spaces')
            continue
        break
    except (ValueError, RuntimeError, TypeError, NameError):
        print("please enter valid name")
while True:
    try:
        weight_lb = float(input("Please enter you weight in pounds: "))
        break                                                     #0 catch not needed for 0 in numerator
    except (ValueError, RuntimeError, TypeError, NameError):
        print("Please enter a valid number")
while True:
    try:
        height_ft = float(input("Please enter you height in feet :"))
        if height_ft != 0:                                          # if statement to catch 0 in denominator
            break
        else:
           print("Please enter non-zero number.")
    except (ValueError, RuntimeError, TypeError, NameError):
        print("Please enter a valid number")


weight_lb = round(weight_lb, 3)
height_ft = round(height_ft, 3)
new_health_file = {'Name':name,'Weight':weight_lb,'Height':height_ft}

User_record.append(new_health_file)
print(User_record)

dataRecorder(filename, User_record)
