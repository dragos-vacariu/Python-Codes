#Each key is separated from its value by a colon (:), the items are separated by
#commas, and the whole thing is enclosed in curly braces. An empty dictionary
#without any items is written with just two curly braces, like this: {}.

#Keys are unique within a dictionary while values may not be. The values of a
#dictionary can be of any type, but the keys must be of an immutable data type
#such as strings, numbers, or tuples.

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

print ("dict['Name']: {0}" .format(dict['Name']))
print ("dict['Age']: {0}" .format(dict['Age']))

#An item can be accessed only with a valid key, trying otherwise will result
#in an error.

#UPDATING DICTIONARY:
print("\nAfter the update:")
dict['Age'] = 8; # update existing entry
dict['Name'] = "DPS School"; # Add new entry
print ("dict['Name']: {0}" .format(dict['Name']))
print ("dict['Age']: {0}" .format(dict['Age']))

#LOOPING THROUGH DICTIONARY:
for name,key in dict.items(): #treat 'name' as the Name(from dictionary)
                        #and key as the Key(value from the dictionary)
    print("Key: ", key, "\t Name:", name)

#DELETING DICTIONARY ITEMS:
del dict['Name']; # remove entry with key 'Name'
#After the deletion the item with key 'Name', accessing it will result and error.
dict.clear();     # remove all entries in dict, the dictionary will be empty.
del dict ;        # delete entire dictionary, it won't exist anymore.




#Dictionary values have no restrictions. They can be any arbitrary Python object,
#either standard objects or user-defined objects. However, same is not true for
#the keys

#IMPORTANT: More than one entry per key not allowed. Which means no duplicate
#key is allowed. When duplicate keys encountered during assignment, the last
#assignment wins.

#Keys must be immutable. Which means you can use strings, numbers or tuples
#as dictionary keys but something like ['key'] is not allowed.

#Example: dict = {['Name']: 'Zara'}

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
