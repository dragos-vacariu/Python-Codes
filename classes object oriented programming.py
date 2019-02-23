#Object Oriented Programming in Python (OOP)

#Documentation:

#Class: A user-defined prototype for an object that defines a set of attributes that characterize any object of the class.
#The attributes are data members (class variables and instance variables) and methods, accessed via dot notation.

#Class variable: A variable that is shared by all instances of a class. Class variables are defined within a class but
#outside any of the class's methods. Class variables are not used as frequently as instance variables are.

#Data member: A class variable or instance variable that holds data associated with a class and its objects.

#Function overloading: The assignment of more than one behavior to a particular function. The operation performed varies
#by the types of objects or arguments involved.

#Instance variable: A variable that is defined inside a method and belongs only to the current instance of a class.

#Inheritance: The transfer of the characteristics of a class to other classes that are derived from it.

#Instance: An individual object of a certain class. An object obj that belongs to a class Circle, for example, is an
#instance of the class Circle.

#Instantiation: The creation of an instance of a class.

#Method : A special kind of function that is defined in a class definition.

#Object: A unique instance of a data structure that's defined by its class. An object comprises both data members (class variables and instance variables) and methods.

#Operator overloading: The assignment of more than one function to a particular operator.

#Creating a class:
class Employee:
   'Common base class for all employees' #This works like documentation of the class.

   #This member is a class variable whose value is shared among all instances of a this class.
   empCount = 0 #this is like a static variable. The class will create only a variable for all the instances.

    #Creating a constructor for the class:
   def __init__(self, name, salary):    #the name of the constructor is always the same: "__init__"

    #Here is the place where the members of the class gets created and initialized.
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self): #The first parameter of any function in the class is always "self"
    #That means that the function will display information about that instance that calls it.
     print ("Total Employee {0}" .format(Employee.empCount))

   def displayEmployee(self):#The first parameter of any function in the class is always "self"
    #That means that the function will display information about that instance that calls it.
      print ("Name : {0}, Salary: {1}" .format(self.name,self.salary))

    #Implementing a destructor for the class.
   def __del__(self):
      #This code will be executed when calling 'del instance'
          class_name = self.__class__.__name__
          print ("Employee destroyed")


#Creating the instances:
"This would create first object of Employee class"
emp1 = Employee("Zara", 2000)
"This would create second object of Employee class"
emp2 = Employee("Manni", 5000)

#Calling the functions;
emp1.displayEmployee()
emp2.displayEmployee()
emp1.displayCount()
Employee.displayCount(emp2) #This can work like this as well. But it needs to be specified an instance
Employee.displayEmployee(emp1)  #This can work like this as well. But it needs to be specified an instance

#Instead of using the normal statements to access attributes, you can use the following functions:
#So there is no need for GETTERS and SETTERS:
hasattr(emp1, 'name')    # Returns true if 'name' attribute exists
getattr(emp1, 'name')    # Returns value of 'name' attribute
setattr(emp1, 'name', "Mark") # Set attribute 'name' at 8
# delattr(empl, 'name')    # Delete attribute 'name'

emp1.displayEmployee()


#Built-In Class Attributes:
#They can be accessed using dot operator like any other attribute,

#__dict__: Dictionary containing the class's namespace.
#__doc__: Class documentation string or none, if undefined.
#__name__: Class name.
#__module__: Module name in which the class is defined. This attribute is "__main__" in interactive mode.
#__bases__: A possibly empty tuple containing the base classes, in the order of their occurrence in the base class list.

#Accesing those attributes:
print ("Employee.__doc__: {0}" .format(Employee.__doc__))
print ("Employee.__name__: {0}" .format( Employee.__name__))
print ("Employee.__module__: {0}" .format( Employee.__module__))
print ("Employee.__bases__: {0}" .format( Employee.__bases__))
print ("Employee.__dict__: {0}" .format( Employee.__dict__))


#Python deletes unneeded objects (built-in types or class instances) automatically to free the memory space.
#Python's garbage collector runs during program execution and is triggered when an object's reference count
#reaches zero. An object's reference count changes as the number of aliases that point to it changes.
#You normally will not notice when the garbage collector destroys an orphaned instance and reclaims its space.

#A class can implement the special method __del__(), called a destructor, that is invoked when the instance is about to
#be destroyed.

#Example:
del emp1 # this will delete the instance callded emp1.
emp2.displayEmployee()
#emp1.displayEmployee() -> not defined anymore

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
