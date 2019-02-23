#Functions in Python:

#A function is a block of organized, reusable code that is used to perform a
#single, related action. Functions provide better modularity for your
#application and a high degree of code reusing.

#IMPORTANT: All parameters (arguments) in the Python language are passed by
#reference. 

def AddingNumbers(a,b):
    return a+b

print("The sum of {0} and {1} is: {2}\n" . format(5,4,AddingNumbers(5,4)))

#ABOVE in the print() function call the AddingNumbers() function is called using
#required arguments

#BELOW the function AddingNumbers() is called using keyword arguments:
print("The sum of {0} and {1} is: {2}" . format(5,4,AddingNumbers(a=5,b=4)))
#Keyword arguments are used to specify for which arguments you are giving a value
#when it comes to default arguments.

#A function can have default arguments:
def PrintFunct (str="Default argument"):
    print(str)
    return

print("This is PrintFunct: {0}" .format(PrintFunct()))

#If you have a function with 2 default arguments, you can use keyword to specify
#for which of them you are setting a value.

def PrintFunct2 (str="Default argument", str2="Default argument2"):
    print("{0} + {1}" .format(str, str2))
    return
print("This is PrintFunct2: ")
PrintFunct2(str="First String")

#The function PrintFunct() above is called using default argument (no value is
#passed).

#Variable-length arguments - > can be implemented using tuples as arguments:
def VarArgFct(arg1, *ArgTuple):
    print("\n")
    print(arg1)
    for item in ArgTuple:
        print("{0}" .format(item))
    return

#Calling function:
VarArgFct(22, 44,33,55)
VarArgFct(22, [44,33,55])


#Anonymous Functions - are called anonymous because they are not declared in
#the standard manner by using the def keyword. You can use the lambda keyword
#to create small anonymous functions.

#Example:
sum = lambda arg1, arg2: arg1 + arg2; #Anonymous functions are small single line functions

#Anonymous functions don't need a 'return' statement, they will return whoever the
#value after the ':' is. (return values similarily as ternary operator)

#Calling the function:
print ("Value of total: {0}" .format(sum(10,20)))

#Variables: local and global.
#Local variables - are those that are declared inside a function.
#Global variables - are those declared outside of any function.

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
