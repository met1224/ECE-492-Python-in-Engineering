# -*- coding: utf-8 -*-
"""calBMI.py


this file takes weight and the height from the user and calculates the body mass index.
BMI is calculated from (Weight(kg))/(Height(m))^2
the weight in the input is in pounds (lbs) and the height is in feet 
"""
try:
	w = float(input("Weight in lbs?  >"))
	h = float(input("Height in feet? >"))


	print (f'Wheight: {w:.3f} (lbs) = {w/2.205:.3f} (Kg)')
	print (f'Height: {h:.3f} (feet) = {h/3.281:.3f} (m)')
	print (f'BMI =  {((w/2.205)/((h/3.281)**2) ):.3f}')

except ValueError:
	print("invalid entry")
except ZeroDivisionError:
	print ("Height can not be zero")