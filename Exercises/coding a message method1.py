from random import randint

def CodingMessage(Message):
    Lst=[]
    i=0
    newStr=""
    #Splitting Message in List and encoding
    while(i<len(Message)):
        if(Message[i] == " "):
            Lst.append(str(i+1)+"_")
        else:
            Lst.append(str(i+1)+Message[i])
        i+=1
    #Randomizing the list and creating the new string:
    while(len(Lst)):
        choice = randint(0, len(Lst)-1)
        newStr+=Lst[choice]
        del Lst[choice]
    #Returning the result:
    return newStr

Message = input ("Enter a string: ")
print()
print("The original message is: ", Message)
print()
print("The coded message is: ", CodingMessage(Message))

#Keep the console opened until the next button pressed.
print()
input("Press any key to quit.")
