#Sets allow only immutable elements


class Persoana:
    def __init__(self, nume, prenume, varsta):
        self.nume = nume
        self.prenume = prenume
        self.varsta = varsta

    #overwriting the == operator
    def __eq__(self, second):
        if self.nume == second.nume and self.prenume == second.prenume and self.varsta == second.varsta:
            return True
        else:
            return False

    def __hash__(self): #the hash function is obliged to return an integer.
        return 1

    def __str__(self):
        return self.nume + "\t" + self.prenume + "\t" + self.varsta

    #this will allow printing in Humanly form
    __repr__ = __str__
s = set()


s.add(Persoana("Popescu", "Ana", "27")) #if the __eq__ operator is overwritten, then the set will not accept objects from that
#class within it.

''' == -> is checking if 2 variable have same values at the address they are poiting too.
    is -> is checking if 2 variable point to the same address.
    when checking 2 objects with "==" unless __eq__ function is ovewritten, it will be replaced by python to "is"
'''

print(s)