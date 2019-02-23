#This program will count the number of vowels in a string.

def getCount(inputStr):
    num_vowels = 0
    # your code here
    SetO = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    for letter in inputStr:
        if letter in SetO:
            num_vowels+=1
    return num_vowels

print("The string has: " + str(getCount(input("Enter a string: ")))+ " vowels.")

#Keep the console opened for the next button pressed:
input("Press any key to quit.")
