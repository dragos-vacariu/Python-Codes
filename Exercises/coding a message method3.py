from random import randint

def CodeMessage(Message):
    Lst =[]
    i=0
    #Splitting string message into list:
    while i< len(Message):
        Lst.append(str(i)+Message[i])
        i+=1
    #Sorting 3 digits and three letters:
    Lst2=[]
    buff=""
    buff2=""
    countRound=0;
    for item in Lst:
        if(countRound==3):
            Lst2.append(buff+buff2)
            buff=""
            buff2=""
            countRound=0;
        for it in item:
            if it >= "0" and it<="9":
                buff+=str(it)
            else:
                if(it == " "):
                    buff2+="_"
                else:
                    buff2+=it
                break
        buff+="#"
        countRound+=1
    if(countRound>0):
        Lst2.append(buff+buff2)
        buff=""
        buff2=""
        countRound=0;
    del Lst
    Message=""
    #Randomizing the list and creating the string.
    while(len(Lst2)):
        choice=randint(0, len(Lst2)-1)
        Message+=Lst2[choice]
        del Lst2[choice]
    #Return the result
    return Message


Message = input("Enter a message: ")
print()
print("The original message is: ", Message)
print()
print("The coded message is: ", CodeMessage(Message))

#Keep the console opened until the next button pressed.
print()
input("Press any key to quit.")
