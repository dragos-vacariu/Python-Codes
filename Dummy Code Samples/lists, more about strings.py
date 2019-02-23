#Accesing an element of a string
StringVar = "This is a string!"

print("The string is: {0}" .format(StringVar))
print("The 8th element of the string is: {0}" .format(StringVar[8]))

#Accesing the last element of the string can be done using StringVar[-1]

print("The last element of the string is {0}" .format(StringVar[-1]))
print("The 8th character is also the -9th character in this case: {0}" . format(StringVar[-9]))

#Slicing strings

#StringVar[2:12] -> will access only from the 2nd index until the 8th index of the string.


#StringVar[:12] -> will access all the elements from the 0th until 12th
#StringVar[3:] -> will access all the elements form the 3th until the last
#StringVar[:] -> will access all the elements of the string

print("This is the string sliced [3:]: {0}" .format(StringVar[3:]))

#Get the length of a string
print("The length of StringVar is: {0}" .format(len(StringVar)))

#Changing multiple items of the string:
StringVar = StringVar[:4] #keep only the first 4 elements of the string.
StringVar += "ABC" #add these elements at the end of it

print("The new string is: {0}\n" .format(StringVar))

#LISTS

CharList = ['M','e','s','s','a','g','e']
#A list is like a vector(dynamic in length) and it can be accessed in the same way, by index.
#In Python a list can be created using any type of data.
#Dynamic length of a list, allows appending new elements at the end of the list,
#so that the size would change automatically.

print('The list is: {0}' .format(CharList))

#Accessing an element of the list:
print('This is the 4th element {0}' .format(CharList[4]))

#Changing an element of the list:
CharList[4] = 'O'
print("The new 4th element is: {0}" .format(CharList[4]))

#Appending elements at the end of the list.
CharList+= ['1', '2'] # this is used for temporarily change.
print("The list now, looks like this: {0}" .format(CharList))
CharList.append('3') # this is used for permanent change. 
print("The list now, looks like this: {0}" .format(CharList))

#Slicing lists:
print("The sliced list is: {0}" .format(CharList[:5])) #slicing a list can be done
#just like in case of strings.

#Changing multiple items of the list:
CharList[2:] = ['2', '3'] #this synthax can only be used on lists, to add multiple
#elements after a given index (will automatically erase the rest of the elements
#after that index)
print(CharList)

#Emptying the list:
CharList[:] = []
print(CharList)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
