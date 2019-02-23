#Zipping (combining) list together.

Lst1 = ["Dragos", "Alan", "Robin"]
Lst2 = ["Blake", "Walker", "Williams"]

names = zip(Lst1,Lst2)

#names will be a new list, a 2D list I might say, containing all the elements in
#Lst1 and Lst2 combined.

#Iterating names:
for a,b in names:
    print("Name = ", a, b)
