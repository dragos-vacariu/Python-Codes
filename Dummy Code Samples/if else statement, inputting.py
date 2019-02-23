varA = 20

#The synthax for if / else statement is:
if varA==20 :
    print("condition is {0}" .format(varA==20))

else :
    print("condition is {0}" .format(varA==20))

#The second way of testing: (using "is" instead of "==" operator)
if varA is 20 :
    print("condition is {0}" .format(varA==20))

else :
    print("condition is {0}" .format(varA==20))

#Comparing strings:
name = "String" #In python each variable needs to be initialized from the beginning
#So that the compiler would know which data type would store.

if name == "String" : #comparing string using == operator
    print("{0} == String" .format(name));
elif name is "" : #comparing string using "is" keyword (it does the same thing
#as == operator)
#elif is used to check for a secondary condition, it runs only
#if the first condition within if statement if false.
    print("{0} is NULL")
else : #the else block runs whenever the first 2 conditions of the if-else chain
#are false.
    print("No option valid.")

#Indentation (the TAB space within a block of code such as: if-else, for, function
#definition), it can be seen above in the if-else statement, the code to be executed
#when the condition is fulfilled is indented with one TAB space from the left margin
#In Python indentetation is more important than it is in any other programming languages
#because the indentation is used to specify the body of a conditional statement(if-else),
#loop,fuction definition and so on.

#The conditional operators that can be used within Python are the same just like in
#any other programming language:
    # "==" -> which checks for equality
    # "<=" -> which checks for lower than, or equal to
    # ">=" -> which checks for higher than, or equal to
    # "!=" -> which checks for not equal to
    # "is" -> which checks also for equality just like "=="
    # "and" -> AND operator is true, only when both conditions are fulfilled
    # "or" -> OR operator is true, only when at least one condition is fulfilled
    # "^" -> XOR operator is true, only when one of the all the condition are fulfilled


#Checking for multiple condition:
if varA==20 and name == "" :
    print("Both conditions are true")
elif varA==20 or name == "String" :
    print("At least one of the conditions are true")

#Checking inputs:
number = input("Enter a number: ")
if int(number) is 1:
    print("Number is 1")
elif int(number) is 2:
    print("Number is 2")
else:
    print("Number is something else.")

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
