#working with sets

a = {"a","b","cd",3,4} # set not indexable, set has only one element of the same value, elements are ordered randomly when program opens
print("a = " + str(a))

#Operations:
b = {"a", "s", "g", 3, 4, 5, 9}
print("b = " + str(b))

print("a-b: " + str(a-b)) #differences from a compared to b
print("b-a: " + str(b-a)) #differences from b compared to

#working with dictionaries:
c = { "d": {12,14}, "14": 14}
print("c = " + str(c))
print(str(c.get("d"))) #get element by key
print(str(c["d"])) #get element by key

# add element to dictionary :
c["key"] = "value"
print(str(c["key"]))
print(c)

#remove element from dictionary
del c["key"]
print(c)

#Formating text
#x = "bala"

#print(f'ala {x} portocala')
print("{}{}{}" .format("a","b", "c")) #access elements in order.
print("{2}{1}{0}" .format("a","b", "c")) #using the index to access elements.
print("{Andrei}, {Marius}" .format(Marius="17 ani", Andrei="2 ani")) #accessing elements by paramater name
print("{Andrei}, {Marius}, {0}, {1}" .format("12", "22",Marius="17 ani", Andrei="2 ani")) #accessing elements by paramater name and index
print("%s %s %s" % ("ala", "bala", "portocala")) #formating text like in c-style
print("%d, %i, %f, %s" % (22, 11, 2.5, "blabla"))

#Comprehensions
#l = [x**2 for x in range[0,10]] # L = Squares withing range 0- 10
#print (l)

input("\nPress ENTER to exit.")