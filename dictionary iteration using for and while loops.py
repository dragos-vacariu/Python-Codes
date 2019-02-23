#Accessing elements of dictionary using index in while loop:
i=0
dict = {"name1": "John", "name2": "Allan", "name3": "Mark"}
#Iterating through dictionary using while loop (FOR VALUES):
while(i<len(dict)):
    print("While-loop Key: ", list(dict.keys())[i], \
                  " While-loop Value: ", list(dict.values())[i])
    i+=1
print()
#Iterating through dictionary using while loop (FOR VALUES):
i=0
while(i<len(dict)):
    print("While-loop Value: ", list(dict.values())[i])
    i+=1
print()
#Iterating through dictionary using while loop (FOR VALUES):
i=0
while(i<len(dict)):
    print("While-loop Key: ", list(dict.keys())[i])
    i+=1
print()
#Iterating through dictionary using for loop (BOTH FOR KEYS AND VALUES):
for n,k in dict.items():
    print("For-Loop key = ", n, " For-Loop Value = ", k)
print()
#Iterating through dictionary using for loop (ONLY FOR KEYS):
for k in dict:
    print("For-Loop key = ", k)
print()
#Iterating through dictionary using for loop (ONLY FOR VALUES):
for k in dict.values():
    print("For-Loop Value = ", k)

#Keep the console opened until the next button pressed:
input("Enter anything to quit.")
