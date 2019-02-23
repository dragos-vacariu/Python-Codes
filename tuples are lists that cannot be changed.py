#A tuple is a sequence of immutable Python objects. Tuples are sequences, just
#like lists. The differences between tuples and lists are, the tuples cannot
#be changed unlike lists and tuples use parentheses, whereas lists use square
#brackets.

tup1 = ('physics', 'chemistry', 1997, 2000);
tup2 = (1, 2, 3, 4, 5 );
tup3 = "a", "b", "c", "d";

#An empty tuple is declared like this:
tup1 = (); #Tuples can be reinitialized with other values.

#To write a tuple containing a single value you have to include a comma, even
#though there is only one value −
tup1 = (50,); 
print("The tuple contain {0} elements: {1} " .format(len(tup1), tup1[0]))

#Like string indices, tuple indices start at 0, and they can be sliced, concatenated,
#and so on.

#Tuples are immutable which means you cannot update or change the values of tuple
#elements. You are able to take portions of existing tuples to create new tuples
#as the following example demonstrates −

tup1 = (12, 34.56); #Tuples can be reinitialized with other values.
tup2 = ('abc', 'xyz');

# Following action is not valid for tuples
# tup1[0] = 100;

# So let's create a new tuple as follows
tup3 = tup1 + tup2;
print (tup3)

#Tuples can be DELETED as follows:
del tup3
#print(tup3) -> this will result an error, tup3 won't exist anymore after its deletion

tup3 = tup1 + tup2;
#Tuples can use the same operation just as lists:
print ("\nExample: tup3[2] = {0}, tup3[-2] = {1}" .format(tup3[2], tup3[-2]))

print("Slicing tuples: {0}" .format(tup3[:2]))
print("Slicing tuples: {0}" .format(tup3[2:]))

#Any set of multiple objects, comma-separated, written without identifying symbols
#are by default set to tuples.
#Examples:
x, y = 1, 2;

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
