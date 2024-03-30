class Person: # for inheritance class Person(parent_class):
    #Static fields are declared here
    name = "name"
    __age = 0 #this is a public field
    width = 0 #this is a private
    #static field can become non-static field for a particular instance at a particular time when specified
    def __init__(self):
        #This is the constructor: Only one constructor function is allowed
        #Function overriding is forbidden
        self.width = 104
        #Non-Static field get declared in the constructor
    def setName(self, Name): # this is a setter
        self.name = Name
    #Encapsulation
    def setAge(self, Age):
        self.__age = Age
    def getAge(self):
        return self.__age

class Employee(Person):
    def __init__(self):
        super().__init__()
        self.name = "Employee"
#Creating a class
person = Person ()
#seting the field of the class
person.setName("Alin Popescu")
#Accesing the public field of the class
print (person.name)

#setting the value of private field
person.setAge(22)
#getting the value of a private field
print(person.getAge())

#accessing field modified by the constructor
print(person.width)

emp = Employee()
print(emp.name)

input("\nPress ENTER to exit.")