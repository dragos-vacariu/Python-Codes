#Unpacking a list of items:

item, name, price = ["Car", "Mustang Gt", "14000"]
#This is an unpacked list, where each element is actually a variable.

print("item: ", item, " name: ", name, " price: ", price);

#The lists that have many more elements:
print("\nThis is the second method: ")
start, *middle, end = ["element1", "element2", "element3", "element4"]
print(start) # this will print the first element
print(*middle) # this will print all the middle elements
print(end) # this will print the last element
