#Class inheritance.

#Instead of starting from scratch, you can create a class by deriving it from a preexisting class by listing the parent class in
#parentheses after the new class name.

#The child class inherits the attributes of its parent class, and you can use those attributes as if they were defined in the
#child class. A child class can also override data members and methods from the parent.

class Parent:        # define parent class

    #Members declared here will be shared through all the instances
    
    #Creating a public member
   parentAttr = 100 #This is a public member which could be accessed from anywhere.

   #Creating hidden (private) member:
   __secretCount = 0 #this member is only visible for this class. So child classes won't be able to access or inherit it.
   #To create hidden members (private members), you just need to put __ as prefix.
   #Private members are only visible inside the class, and can be accessed only by class instances. IT DOES NOT INHERIT.


   #Defining a constructor:
   def __init__(self):

       #Members declared here will be individually created for each instance:
      print ("Calling parent constructor")
         #Creating protected member(variable):
      self._protectedVar = 2 # protected variables can be accessed by parent class and child class, they are not public.
        #Creating hidden (private) member:
      self.__privateVar = 1

   def parentMethod(self):
      print ("Calling parent method")
      
    #Defining a setter:
   def setAttr(self, attr):
      Parent.parentAttr = attr
      
    #Defining a getter:
   def getAttr(self):
      print ("Parent attribute : {0}" .format(Parent.parentAttr))

   def myMethod(self):
      print ("Calling parent method")
   def printPrivate(self):
       print("Private Variable: {0}" .format(self.__privateVar))

class Child(Parent): # define child class
    #Defining a contructor:
   def __init__(self):
      print ("Calling child constructor")
      Parent.__init__(self)
   def childMethod(self):
      print ("Calling child method")

    #This is an overrided function:
   def myMethod(self):
      print ("Calling the overrided method.")

c = Child()          # creating an instance of Child class
c.childMethod()      # child calls its method
c.parentMethod()     # calls parent's method
c.setAttr(200)       # again call parent's method
c.getAttr()          # again call parent's method

#Functions:
#The issubclass(sub, sup) boolean function returns true if the given subclass sub is indeed a subclass of the superclass sup.

#The isinstance(obj, Class) boolean function returns true if obj is an instance of class Class or is an instance of a
#subclass of Class

#You can always override your parent class methods. One reason for overriding parent's methods is because you may want
#special or different functionality in your subclass.
c.myMethod()

#Trying to print a private member:
#print("Private value: {0}" .format(c.__secretCount)) -> compilation error, child has no member named like that.
#print("Private value: {0}" .format(Parent.__secretCount)) -> compilation error, parent has no member like that.

print("The public member: {0}" .format(Parent.parentAttr))
#print("The protected member: {0}" .format(Parent._protectedVar)) -> compilation error, parent class has no member name like that.
print("The protected member: {0}" .format(c._protectedVar))
p1 = Parent()
#Accesing the private variable can only be made with public accessors (Getters and Setters)
p1.printPrivate()
#print("The private member: {0}" .format(p1.__privateVar)) -> this won't work.

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
