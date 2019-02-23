class Girl:
    #This is a class variable, it will be the same for each instance.
    gender = "female"

    def __init__(self, name):
        #This is a instance variable, it will be unique for each instance.
        self.name=name

#A class variable is like a static variable in C#, C++, Java, so the variable
#will be shared amongst all of the instances. Whereas a instance variable is
#unique to all of the instances.
girl1 = Girl("Rachel")
girl2 = Girl("Madonna")
print("Name: ", girl1.name, " Gender: ", girl1.gender)
print("Name: ", girl2.name, " Gender: ", girl2.gender)
