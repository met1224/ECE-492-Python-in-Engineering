# -*- coding: utf-8 -*-
"""
Created on Tuesday May 23 13:30:00 2023

@author: Byron K Nelson
This program calculates Body Mass Index (BMI) of the user-entered values. It takes in weight in pounds
and height in feet and then converts them to metric to make the necessary calculation.
  
  -Inputs: Weight in Pounds, Height in Feet
  -Output: The Body Mass Index

"""

def calcBMI(w, h):
    """
    This function actually performs the calculation of BMI.

    -Inputs: Weight in Pounds, Height in Feet
    -Output: The Body Mass Index
  
    """
    bmi = w / (h**2)
    return bmi

# Prompt User for Weight in Pounds
try:
    w = int(input("Please Enter the Weight in Pounds: "))
except (ValueError, RuntimeError, TypeError, NameError):
    print("Invalid Entry")
    exit(-1)

# Prompt User for Height in Feet
try:
    hf = int(input("Please Enter the Height in Feet: "))
except (ValueError, RuntimeError, TypeError, NameError):
    print("Invalid Entry")
    exit(-1)
    
# Prompt User for Height in Inches
try:
    hi = int(input("Please Enter the Additional Height in Inches: "))
except (ValueError, RuntimeError, TypeError, NameError):
    print("Invalid Entry")
    exit(-1)

# Convert Weight From Pounds to Kilograms
w_kg = w * 0.453592

# Calculate the Total Height in Inches
h_tot = (hf * 12) + hi

# Convert Height to Metric
h_m = h_tot * 0.0254

if h_m == 0 or w_kg == 0:
    print("Invalid Weight or Height!")
    exit(0)
    
# Calculate the BMI by Calling Function calcBMI()
bmi = calcBMI(w_kg, h_m)

# Print the Results With 3 Decimal Digit Precision
print("Weight = {:} lbs = {:.3f} Kg".format(w, w_kg))
print("Height = {:} feet {:} inches = {:.3f} m".format(hf, hi, h_m))
print("BMI = {:.3f}".format(bmi))