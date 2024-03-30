#The next line will set the filepath:
PYTHONPATH=r'C:\Users\Black2\Desktop\python\modular programming in python'
#The next line will import a specific module:
import module_with_functions

#Calling functions from inside the module:
module_with_functions.print_func("Dragos")

print("Sum of {0} and {1} is: {2}" .format(4,10,module_with_functions.CalculateSum(4,10)))

#There is possible to import a single function from the whole module below is the
#synthax:
from module_with_functions import print_func
#The effect is here: the fuction can be called without mentioning the module, whereas
#in the example above it couldn't.
print_func("Black")

#The following synthax will import anything from the mentioned module:
from module_with_functions import *

print("{0}+{1}={2}" .format(3,4,CalculateSum(3,4)))
#Once again there was no need of mentioning the module for CalculateSum()


#Namespace and scoping:
#Variables are names (identifiers) that map to objects. A namespace is a dictionary
#of variable names (keys) and their corresponding objects (values).

#A Python statement can access variables in a local namespace and in the global
#namespace. If a local and a global variable have the same name, the local
#variable shadows the global variable.

#Python makes educated guesses on whether variables are local or global. It
#assumes that any variable assigned a value in a function is local.
#Therefore, in order to assign a value to a global variable within a function,
#you must first use the global statement.

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
