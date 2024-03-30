#clasa PUNCT cu 2 parametri x, y
#clasa CERC mosteneste PUNCT, si defineste o raza
#CERC are o metoda de calculul a ariei

class PUNCT:
    #constructor
    def __init__(self, xCoord, yCoord):
        self.x=xCoord #non-static field
        self.y=yCoord #non-static field

    #public method
    def calculateDistance(self, Punct):
        distanceX = Punct.x - self.x
        distanceY = Punct.y - self.y
        distance = (distanceX**2) + (distanceY**2)
        return distance ** 0.5

    #operator overloading
    def __add__(self, other): #overloading the "+" operator for addition
        if(isinstance(other, POLYLINIE)):
            points = [self]
            for x in other.Points:
                points.append(x)
            return POLYLINIE(*points)
        else:
            polilinie = POLYLINIE(self, other)
            return polilinie

    #built-in function overloading
    def __str__(self):
        return "Punct(" +str(self.x) + ", " +str(self.y) +")"


class CERC(PUNCT): #CERC inherits from PUNCT
    #constructor
    def __init__(self, Punct, Rad):
        super().__init__(Punct.x, Punct.y) #super() returns the parent class
        self.Radius = float(Rad)

    #public methods
    def getArea(self):
        return 3.14 * self.Radius**2

    def calculateDistanceToObject(self, Data):
        if isinstance(Data, CERC):
            return super().calculateDistance(Data) - self.Radius - Data.Radius
        elif isinstance(Data, PUNCT):
            return super().calculateDistance(Data) - self.Radius


class SEGMENT(PUNCT):
    def calculateDistance(self, Punct1, Punct2):
        distanceX = Punct2.x - Punct1.x
        distanceY = Punct2.y - Punct1.y
        distance = (distanceX**2) + (distanceY**2)
        return distance ** 0.5

    #constructor
    def __init__(self, Punct1, Punct2):
        super().__init__(Punct1.x, Punct1.y)
        super().__init__(Punct2.x, Punct2.y)
        self.length = self.calculateDistance(Punct1,Punct2)

    #build-in function overloading
    def __str__(self): #redefining the function __str__ so it can be printed directly print(obj)
        return "Length of segment: " + str(self.length)

    #Operator overloading
    def __gt__(self, other): #overloading > operators (gt comes from greater)
        return self.length < other.length
        #also work for <, because of negations

    def __ge__(self, other): #overloading >= operators (ge comes from greater than or equal to)
        return self.length < other.length
        #also work for <= because of negations

    def __eq__(self, other): #overloading == operator
        return self.length == other.length


class POLYLINIE:
    #constructor
    def __init__(self, *Points):
        self.Points=list(Points)

    #built-in function overloading
    def __str__(self):
        value="Polilinie("
        for p in self.Points:
            value+=str(p)+", "
        value+=")"
        return value

    #operator overloading
    def __add__(self, other): #overloading the "+" operator for addition
        puncte = []
        for x in self.Points:
            puncte.append(x)
        puncte.append(other)
        return POLYLINIE(*puncte)

    def __iter__(self): #making class iterable
        self.counter=0

    def __next__(self): #making clas iterable
        if self.counter < len(self.Points):
            self.counter+=1
        else:
            raise Exception ("Object reached boundaries")

x = 3;    y = 4
#x = float(input("p1.x: "))
#y = float(input("p1.y: "))
punctUnu = PUNCT(x,y)

cerc = CERC(punctUnu, Rad = 2.0)

x = 5;    y = 6
#x = float(input("p2.x: "))
#y = float(input("p2.y: "))

punctDoi = PUNCT(x,y)

cerc2 = CERC(punctDoi, Rad = 3.0)

print("\nArea of circle = " + str(cerc.getArea()))
print("Distance PointToPoint = " + str(punctUnu.calculateDistance(punctDoi)))
print("Distance CircleToPoint = " + str(cerc.calculateDistanceToObject(punctDoi)))
print("Distance CircleToCircle = " + str(cerc.calculateDistanceToObject(cerc2)))

segment = SEGMENT(punctUnu, punctDoi)
print(segment)
segmentSec = SEGMENT(punctDoi, PUNCT(10,7))

print() #put a new line
print(segmentSec)
print(segment < segmentSec)
print(segment >= segmentSec)
print(segment == segmentSec)

print() #put a new line
polyline = POLYLINIE(punctUnu, punctDoi)
#print(polyline)

print("Result: ")

polylineDoi = punctUnu + (punctDoi + punctUnu) # building a polyline from 3 points
print(polylineDoi)
