#Sorting the items(letters) of a string in alphabetical order.

def AlphabetSoup(str): 
    # code goes here
    Lst=[]
    #Converting string to List:
    for letter in str:
        Lst.append(letter)
    strLen=len(Lst)
    i=0
    #Arranging the list:
    while(i<strLen):
        j=0
        while(j<strLen):
            if(Lst[i] < Lst[j]):
                aux = Lst[i]
                Lst[i] = Lst[j]
                Lst[j] = aux
            j+=1
        i+=1
    str=""
    #Converting the list back to string:
    for letter in Lst:
        str+=letter
    return str
    
# keep this function call here  
print (AlphabetSoup(input("Enter a string: ")))

#Keep the console open until the next button press:
input("Press any key to quit: ")
