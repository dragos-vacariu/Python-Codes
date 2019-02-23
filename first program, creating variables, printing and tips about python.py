# Using the # sign to add comments

#This function will print "This is the first Python program" message in the console.
print('This is the first Python program.')


#Adding 2 numbers together.

#When creating variables you don't need a data type, all you need is an identifier (name).
num1 = 1.5 #Creating a variable num1
num2 = 6.3 #Creating a variable num2

# Add two numbers
sum = float(num1) + float(num2)
#sum variable will store the addition result of the num1 and num2 variables converted
#to float

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))

#to display variable's values using print function, the placeholder is used:
#{0}, {1} {2}, just like in C# language.

#.format(num1, num2, sum) specifies which variable's values should be replaced
#with the placeholders and the order within () is respected.

print("\nThis message is also valid.\n");

#To simply display the value of a variable this synthax can be used:
print(sum) # note that semi-colon at the end of the statement is optional.

#Stuff about python below:

#The structure of a Python program is simpler: you don't need an entry point
#to the application (you don't need a main() function). The code is executed
#from the first line until the last line.

#Python is a powerful high-level, object-oriented programming language created by
#Guido van Rossum.

#Some python tips:

#You don't need to define the type of a variable in Python. Also, it's not necessary
#to add semicolon at the end of the statement.

#Python enforces you to follow good practices (like proper indentation). These small
#things can make learning much easier for beginners.

#Python allows you to write programs having greater functionality with fewer lines of code.

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
