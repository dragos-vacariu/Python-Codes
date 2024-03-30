#Creating a Functor class

class Functor:
    #Dunder functions are pre-defined functions which have __ (underscore) as prefix and surfix. Example: __init__()
    def __init__(self, word):
        self.word = word

    #A class became a functor if this function __call___ gets overwritten/defined.
    def __call__(self): #this will make Functor class be a functor.
        print("Functor called.")

obj = Functor("something")
obj() #A functor is callable, just as a function.
obj.__call__() # obj() as functor is equivalent to calling obj.__call__().

print("\nSorting list exercise:")

class Persoana:
    def __init__(self, nume, prenume, varsta):
        self.nume = nume
        self.prenume = prenume
        self.varsta = varsta
    def print(self):
        print(self.nume + "\t\t" + self.prenume + "\t\t" + str(self.varsta))

def main():
    persoane = [
                Persoana("Geere", "Richard", 64),
                Persoana("Walker", "Alan", 24),
                Persoana("Manson", "Mary", 34),
                Persoana("Manson", "Deny", 36),
                Persoana("Menance", "Denise", 54),
                Persoana("Reyes", "Antonio", 22),
            ]
    raport_varsta(persoane)
    raport_NumeVarsta(persoane)
    raport(persoane, "nume prenume varsta")

def raport_varsta(persons):
    persons.sort(key=lambda Person: Person.varsta)
    for x in persons:
        x.print()
    print()

def raport_NumeVarsta(persons):
    persons.sort(key=lambda Person: (Person.nume,Person.varsta))
    for x in persons:
        x.print()
    print()

def raport(persons, strV):
    words = strV.split(" ")
    if "nume" in words and "prenume" in words and "varsta" in words:
            persons.sort(key=lambda Person: (Person.nume, Person.prenume, Person.varsta))
    elif "nume" in words and "prenume" in words:
        persons.sort(key=lambda Person: (Person.nume, Person.prenume))
    elif "nume" in words and "varsta" in words:
        persons.sort(key=lambda Person: (Person.nume, Person.varsta))
    elif "prenume" in words and "varsta" in words:
        persons.sort(key=lambda Person: (Person.nume, Person.varsta))
    else:
        if words[0] == "nume": persons.sort(key=lambda Person: (Person.nume))
        elif words[0] == "prenume": persons.sort(key=lambda Person: (Person.prenume))
        else: persons.sort(key=lambda Person: (Person.varsta))
    for x in persons:
        x.print()
    print()

main()
input("Press any RETURN to exit.")