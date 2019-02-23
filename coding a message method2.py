from random import randint

def CodingMessage2(Message, key):
    Lst=[]
    i=0
    newStr=""
    #Splitting Message in List and encoding
    Lst.append(str(key)+"{")
    while(i<len(Message)):
        ch = randint(0,1)
        if(Message[i] == " "):
            if(ch==1):
                Lst.append(str(key-i)+"_")
            else:
                Lst.append(str(key+i)+"_")   
        else:
            if(ch==1):
                Lst.append(str(key-i)+Message[i])
            else:
                Lst.append(str(i+key)+Message[i])
        i+=1
    #Randomizing the list and creating the new string:
    newStr+=Lst[0]
    del Lst[0]
    while(len(Lst)):
        choice = randint(0, len(Lst)-1)
        newStr+=Lst[choice]
        del Lst[choice]
    newStr+="}"
    #Returning the result:
    return newStr

Message = input ("Enter a string: ")
print()
key = int(input("Enter a key for the second method: "))
print()
print("The coded message is: ", CodingMessage2(Message, key))

#Keep the console opened until the next button pressed.
print()
input("Press any key to quit.")
