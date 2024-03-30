listOfObj = list()

items = int(input("Number of items to be added: "))
while items > 0:
    listOfObj.append(int(input("item: ")))
    items-=1

for i in range(0, len(listOfObj)):
    for j in range (i+1, len(listOfObj)):
        if listOfObj[i] < listOfObj[j]:
            listOfObj[i] = listOfObj[i] ^ listOfObj[j]
            listOfObj[j] = listOfObj[i] ^ listOfObj[j]
            listOfObj[i] = listOfObj[i] ^ listOfObj[j]
print(listOfObj)

input("\nPress ENTER to exit.")