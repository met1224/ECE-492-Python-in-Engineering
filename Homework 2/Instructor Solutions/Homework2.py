"""
#Created on Friday May 21 2022

# @author: Justin Kaylor
# This is a program to call functions for: (Print a secret word in a file of random characters
#, Find a word in a file and count the frequency and index location of the word
#,and input a dictionary list to a csv file for health data 

"""

def gen_code_file(secretword: str ="secretword", freq :int =0, maxlength:int = 100000):
    """
    #Fuction that takes in a secret word that gets input into a file of random
    #ascii letters. other variables allow control of freqency of secret word and
    #maxlength of the file. stored in file randon_letters_new.txt
    """

    import string
    import random
    import datetime

    fname = "random_letters_new.txt"                      #name of txt file to be written can be changed here
    while True:
        try:
            secret_word_date = secretword + str(datetime.date.today())      # make sure secretword is a string and add the date to be used in the first instance
            break
        except(ValueError,NameError,TypeError):
            print("secretword is not a string, please pass a string")
            return -1
    if len(secretword) > 16:                                               # if longer than 16 characters tell user it is to long
        print('Please enter a secretword no longer than 16 characters')
        return -1
    
    if freq > (maxlength/(len(secretword)*3)):                             # for edge case of long word with many freq and short maxlength
        print ("Frequency is too high for the specified word to be written to file ")
        return -1
    
    secret_counter = int(freq)
    recharge_linecounter = 200
    counter = maxlength
    linecounter = recharge_linecounter
    
    new_file = ""
    if freq == 0:                                       # used to catch frequency of 0
        random_range = maxlength -1                      #cannot divide by 0 so have to filter out in case of freq = 0
    else:
        random_range = round(int(maxlength)/(int(freq)*1.3))
    
    while counter > 0:
        rando = random.randint(0,(random_range) )
        if rando == 51 and secret_counter > 0:

            if secret_counter == int(freq):
                for i in secret_word_date:                     # first instance gets date added
                    if linecounter <= 0:
                        new_file += ("\n")
                        counter = counter - 1
                        linecounter = recharge_linecounter
                    else:
                        new_file += i
                        counter = counter - 1
                        linecounter = linecounter - 1

            else:
                for i in secretword:                           # word is written 1 letter at a time and a newline added if over 200 characters
                    if linecounter <= 0:
                        new_file += ("\n")
                        linecounter = recharge_linecounter
                        counter = counter - 1
                    else:
                        new_file += i
                        counter = counter - 1
                        linecounter = linecounter - 1
            secret_counter -= 1

        elif linecounter == 0:
            new_file += "\n"
            linecounter = recharge_linecounter
            counter = counter - 1
        else:

            new_file += random.choice(string.ascii_letters)

            counter = counter- 1
            linecounter = linecounter - 1
    print(len(new_file))
    f =open(fname, 'w')
    f.write(new_file)
    f.flush()                          #was having trouble with program hanging so used flush command
    f.close()
    return
    
    
def findWord(filename:str, word:str ='default'):
    """
    #Funcition takes in a filename.txt and a word. then scan the text file for the number
    #of times the word is used in the file and the index location
    """
    
    import os

    
    # path = os.path.join(user_file) used if moving between os systems (mac/linux/windows)
    while True:
        try:
            path = str(filename)
            break
        except(ValueError,NameError,TypeError):
            print("filename is not correct please edit")
            return -1
    while True:
        try:
            word = str(word)
            break
        except(ValueError,NameError,TypeError):
            print("word is not a string, please pass a string")
            return -1
    file = os.path.exists(filename)
    index_list =[]
    if file is True:
        f = open(filename, 'r')
        new_file = ""
        for line in f:
            stripped = line.strip()               # strip off retuen and newline
            stripped = stripped.strip(" ")
            stripped = stripped.strip(('\t'))
            new_file += stripped

        index = 0

        while index < len(new_file):
            index = new_file.find(word, index)
            if index == -1:
                break
            index_list.append(index+1)
            index += 1
        print('word found at index: ',index_list)
        f.close()
        return index_list
    else:
        print("File not found. make sure to add extension on end of file name (ex filename.txt) or enter as string with quotes 'filename.txt'")
        return -1
    
def dataRecorder(filename: str, record: dict):
    """
    #Function takes filename.csv and a dict{Name:name,Weight:weight,Height,height}
    #and either creates a new csv file if one does not exist or appends to a csv file
    """
    
    import os
    import csv

    header_row = ['Name', 'Weight', 'Height']

    file = os.path.exists(filename)

    if file is False:
        with open(filename, 'w', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=header_row)
            writer.writeheader()
            for data in record:
                writer.writerow(data)
        csvfile.close()

    else:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header_row)
            for data in record:
                writer.writerow(data)
        csvfile.close()

    