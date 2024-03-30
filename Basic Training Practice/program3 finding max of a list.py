elements = list()

items = int(input("Number of items to be added: "))
while items > 0:
    elements.append(int(input("item: ")))
    items-=1

max = elements[0]
i=0
while(i < len(elements)) :
    if(max<elements[i]) :
        max=elements[i]
    i+=1

print("\nMAX este: " + str(max) )