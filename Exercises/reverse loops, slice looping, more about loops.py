cars = ["Mitsubishi", "Subaru", "Peugeot", "Renault", "Lamborghini", "Ferrari"]

#Printing the reverse list:
for i in range (5,-1, -1):
    print("{0}" .format(cars[i]))

#Printing the reverse list 2 by 2:
print()
for i in range (5,-1, -2):
    print("{0}" .format(cars[i]))

#Printing the list 2 by 2:
print()
for i in range (0,6, 2):
    print("{0}" .format(cars[i]))    

#Slicing a loop:
print()
for car in cars[:3]:
    print("{0}" .format(car))

#Same syntax for a while:
i=0;
print()
while (i<10):
    print(i)
    i+=2

#Another way of for looping:
print()
for i in range (3):
    print (i)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
