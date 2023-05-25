# -*- coding: utf-8 -*-
"""
Created on Tuesday May 23 16:18:00 2023

@author: Byron K Nelson
This program contains multiple functions as specified by the Homework 1 instructions. Their specifications are as follows:
  
  2. Function to print message Pyramid
  3. Function to find perfect square numbers 
  4. Function to calculate salary 
  5. Function to calculate letter grade 

"""

import math

# Number 2
def pyramid(s):
    """
    Prints a “message pyramid” for the input message string starting from the first character in the string. 

    -Input: One word as a string
    -Output: A visual representation of that string as a pyramid 
  
    """
    if not isinstance(s, str):
        print("Invalid Input. Please Enter a String!")
        return -1
        
    for i in range(1, len(s) + 1):
        print(s[:i])
        
# Example Usage
#message = "potato"
#pyramid(message)

# Number 3
def findSquares(s:int, e=None):
    """
    In the range of the two arguments, this funtion finds and prints the exact squares of an integer.
    
    -Inputs: Two integers representing the range of the list 's' is the starting point and 'e' is the optional endpoint
    -Output: Returns a list of perfect squares in specified range
    """
    if e is None:
        e = s
        s = 0
        
    L = []
    for num in range(s, e + 1):
        root = math.isqrt(num)
        if root * root == num:
            L.append(num)
        
    L.sort()        
    return L
    
# Example Usage
#findSquares(47, 100)

# Number 4
def calSalary(h, r=20):
    """
    This function calculates the salary based on the number of hours and hourly rate.

    -Inputs: Two floats representing the number of hours worked and the hourly rate. The hourly rate defaults to 20
    -Output: The calculated salary as a float
    """
    if h < 0:
        print("Not Valid Hours")
        return -1

    if h <= 40:
        salary = h * r
    else:
        overtime = h - 40
        salary = (40 * r) + (overtime * r * 1.2)

    return salary

# Example Usage
#hours = 30
#rate = 20
#salary = calSalary(hours, rate)
#print("${:.2f}".format(salary))

#hours = 45
#salary = calSalary(hours)
#print("${:.2f}".format(salary))

# Number 5
def calLetterGrade(points, gradescale=None):
    """
    This function calculates the letter grade based on the points and the gradescale.

    -Inputs: The points obtained & the gradescale. The gradescale defaults to None
    -Output: The calculated letter grade
    """
    if not isinstance(points, (int, float)):
        return -1

    if gradescale is None:
        # Default Gradescale from Pie Class Grading Policy Scale
        gradescale = [98, 94, 91, 88, 85, 82, 79, 76, 73, 70, 67, 64]

    if len(gradescale) > 12:
        return -1

    if any(not isinstance(g, (int, float)) for g in gradescale):
        return -1

    if len(gradescale) != len(set(gradescale)):
        print("Gradescale Has Repeat Entry")
        return -1

    gradescale.append(float('-inf'))  # Add Lowest Grade Placeholder

    for i in range(len(gradescale) - 1):
        if points >= gradescale[i]:
            return getGrade(i, len(gradescale) - 2)

    return 'F'


def getGrade(index, max_index):
    """
    This function gets the letter grade based on the index and the maximum index.

    -Inputs: The index position of the grade & the maximum index position in the gradescale
    -Output: The calculated letter grade
    """
    grade_letters = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
    return grade_letters[index] if index <= max_index else 'F'

# Example Usage
#points = 77
#gradescale = [98, 94, 91, 88, 85, 82, 82, 80]
#letter_grade = calLetterGrade(points, gradescale)
#print(letter_grade)