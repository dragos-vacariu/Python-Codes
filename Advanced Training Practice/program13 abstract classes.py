from abc import ABC, abstractmethod


class Insert:
    def do(self): pass

class Delete:
    def do(self): pass

class Append():
    def __init__(self):
        self.do = "Something"


def work(classobj):
    if hasattr(classobj, "do") and callable(getattr(classobj, "do")):
        print("Class OK.")
    else:
        print("Class NOK.")

objA = Insert()
objB = Delete()
objC = Append()

work(objA)
work(objB)
work(objC)

#Abstract classes

class Command(ABC):
    @abstractmethod
    def do(self): pass

class Instruction(Command):
    pass

def checkCommand(obj):
    if isinstance(obj, Command):
        print("Test passed.")

try:
    objIns = Instruction() #this will generate expresion.
    checkCommand(objIns)
except:
    print("Exception caught.")

def xDo(x):
    print("This is the do.")

class InstructionConcrete(Command):
    def do(self):
        print("The do.")

objIns = InstructionConcrete()
checkCommand(objIns)
input("Press any RETURN to exit.")