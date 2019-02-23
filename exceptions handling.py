#Exceptions handling:

#EXCEPTION NAME	DESCRIPTION
#Exception	Base class for all exceptions
#StopIteration	Raised when the next() method of an iterator does not point to any object.
#SystemExit	Raised by the sys.exit() function.
#StandardError	Base class for all built-in exceptions except StopIteration and SystemExit.
#ArithmeticError	Base class for all errors that occur for numeric calculation.
#OverflowError	Raised when a calculation exceeds maximum limit for a numeric type.
#FloatingPointError	Raised when a floating point calculation fails.
#ZeroDivisionError	Raised when division or modulo by zero takes place for all numeric types.
#AssertionError	Raised in case of failure of the Assert statement.
#AttributeError	Raised in case of failure of attribute reference or assignment.
#EOFError	Raised when there is no input from either the raw_input() or input() function and the end of file is reached.
#ImportError	Raised when an import statement fails.
#KeyboardInterrupt	Raised when the user interrupts program execution, usually by pressing Ctrl+c.
#LookupError	Base class for all lookup errors.
#IndexError     Raised when an index is not found in a sequence.
#KeyError       Raised when the specified key is not found in the dictionary.
#NameError	Raised when an identifier is not found in the local or global namespace.
#UnboundLocalError   Raised when trying to access a local variable in a function or method but no value has been assigned to it.
#EnvironmentError   Same as above
#IOError        Raised when an input/ output operation fails, such as the print statement or the open() function when trying to open
#a file that does not exist.
#IOError    Same as above.
#SyntaxError    Raised when there is an error in Python syntax.
#IndentationError   Raised when indentation is not specified properly.
#SystemError	Raised when the interpreter finds an internal problem, but when this error is encountered the Python interpreter does not exit.
#SystemExit	Raised when Python interpreter is quit by using the sys.exit() function. If not handled in the code, causes the interpreter to exit.
#TypeError	Raised when an operation or function is attempted that is invalid for the specified data type.
#ValueError	Raised when the built-in function for a data type has the valid type of arguments, but the arguments have invalid values specified.
#RuntimeError	Raised when a generated error does not fall into any category.
#NotImplementedError	Raised when an abstract method that needs to be implemented in an inherited class is not actually implemented.


#An exception is an event, which occurs during the execution of a program that disrupts the normal flow of the program's
#instructions. In general, when a Python script encounters a situation that it cannot cope with, it raises an exception.
#An exception is a Python object that represents an error.

#Handling exceptions:
try:
   fh = open("dragos1.txt", "a")
   fh.write("This was added by 'handling exceptions' Program.")
except IOError:
   print ("Error: can't find file or read data from {0}" .format(fh.name))
else:
   print ("Written content in the file successfully!")
   fh.close()

#Example 2:
try:
    fh = open("dragos.txt", "r")
    fh.read(12)
except IOError:
    print ("Error: can\'t find file or read data from {0}" .format(fh.name))
finally:
    print ("Not working!")

#When an exception is thrown in the try block, the execution immediately passes to the finally block. After all the statements
#in the finally block are executed, the exception is raised again and is handled in the except statements if present in the
#next higher layer of the try-except statement.

#You can raise exceptions in several ways by using the raise statement. The general syntax for the raise statement is as follows.

level=1
if level < 1:
      raise Exception('level < 1')

#Creating user-defined exception:
class MyError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

#Catching user-defined exceptions:
try:
    raise MyError(2*2)
except MyError as e:
     print ("My exception occurred, value: {0}" .format (e.value))


#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
