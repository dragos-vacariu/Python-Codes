from p19_abs_class import PUNCT as abstract, PUNCT

#p = PUNCT()  #cannot be done, abstract classes cannot be instraciated

class LINE(PUNCT):
    def abstract_method(self): #providing definition for abstract parent method
        print("Abstract method is now redefined")

    #creating static methods:
    @staticmethod #the following method will be static. Static = shared among the instances.
    def staticMe(): #static method don't take self as argument
        print("\nThis is a static method\nAll instances of the class share same method")

l = LINE()

l.abstract_method()
l.staticMe()
#static methods can be invoked only with the class name

LINE.staticMe()