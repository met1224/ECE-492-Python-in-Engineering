#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:42:32 2019

@author: Rags

These are answers to Homework 1
"""

import math

def pyramid(s):
    """ takes the string input and prints a message pyramid """
    try:
        n = str(s)
        for i in range(0, len(n)+1):
            print(n[0:i])
        print()
    except:
        print('invalid entry')


def findSquares(start:int, end:int=0):
    """ This function finds perfect squares between the given two numbers"""
    l = []
    if end < start:
        start, end = end, start
    else:
        pass
    start = max(0, start)
    if end < 0:
        return l
    starti = math.ceil(start ** 0.5)
    endi = int(end ** 0.5)
    for i in range(starti, endi+1):
        l.append(i**2)
#    if 0 in l:                  # This is upto the application whether 0 should be considered a square or not
#        l.remove(0)
    print(l)
    return l

def calSalary(h : float, r: float = 20.0) -> float:
    """ the function will return -1 for errors"""
    if h < 0 :
        print("Not valid Hours")
        return -1
    else:
        S = h * r
        if h > 40:
            S = S + (h-40)*r*0.2
    return S


def calLetterGrade(marks, gradetable:list = [98, 94, 91, 88, 85, 82, 79, 76, 73, 70, 67, 64]):
    """ calculates letter grade based on the marks and the gradetable. grade table should have ideally 12 values corresponsing to A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-.
    Everything lower than D- is F. However if you define the gradeable with fewer values the lowest grade is F"""
    try:
        lettergrade = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        if len(gradetable) > 12:
            print("too many entries in gradescale list, There is no F+ ?")
            return -1
        else:
            newlettergrade = list()
            for i in range(len(gradetable)):
                newlettergrade.append(lettergrade[i])
            newlettergrade.append("F")
        grade = newlettergrade[len(gradetable)]
        if len({x for x in gradetable if gradetable.count(x) > 1}) != 0:
            print('duplicate entry in gradetable')
            return -1

        if isinstance(marks, int) or isinstance(marks, float):
            for i in range(len(gradetable)):
                if isinstance(gradetable[i], int) or isinstance(gradetable[i], float):
                    if marks >= gradetable[i]:
                        grade = newlettergrade[i]
                        break
                else:
                    print('invalid entry in gradescale')
                    return -1
            return grade
        else:
            print("invalid points argument")
            return -1
    except (NameError, SyntaxError):
         print("Invalid entry")
         return -1

