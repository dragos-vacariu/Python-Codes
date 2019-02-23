import math #importing the library called math used for sqrt() function.

#Creating variables

num1 = 25
num2 = 5

print("{0} - {1} = {2}" .format(num1, num2, num1-num2)) #print() function will automatically
#add an \n (line terminator) after the message is print.

#Arithmetic operators:

num1 +=num2
print("Same shortcuts +=, -=, *=, /= from C, C++, C#, Java are still working in Python.\n")
print("{0} += {1} = {2}" .format(num1-num2, num2, num1))

# These synthaxs doesn't work anymore: num1-- , num1++
print("{0}-=1 is {1}, --,++ shortcuts are not available anymore.".format(num1+1, num1))

num1=num1-10
print("{0} - 10 = {1}" .format(num1+10,num1))

num1*=2
print("{0} * 2 = {1}" .format(num1/2, num1))

num1/=2
print("{0} / 2 = {1}" .format(num1*2, num1))

num1+=1
#New operators:
num1 = num1 // 2 #will divide num1 by 2 and take only the integer part of the result

print("{0} // 2 = {1}" .format((num1*2)+1, num1))

num1 = num1 ** 2 #will raise the value of num1 to the power of 2.

print("{0} ** 2 = {1}".format(math.sqrt(num1), num1))

#math.sqrt() -> is a function to calculate the square-root of a value.


#Escaping characters
print('I don\'t like here.') # \ is used as escape character for ' from word don't
print(r'\n - This is escaped character.') # r in front of a string will treat each
#symbol or set of symbols such us '\n' just as normal text.


#Strings
VarString = "Adam"
VarHello = "Hello, "
VarExclamationMark = "!"

#Concatenating strings
print(VarHello+VarString+VarExclamationMark)

#Appending strings
VarHello+=VarString
VarHello+=VarExclamationMark

print(VarHello)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
