from random import randint

def DecodeMessage(Message):
    i=0
    Lst2=[]
    Lst = []
    buff=""
    indexOf=0;
    for letter in Message:
        Lst2.append(letter)
        if(letter < "0" or letter > "9") and (letter != "#"):
            Lst.append(" ")
    #Splitting string message into list:
    while i < len(Lst2):
        if( Lst2[i] == "#" ):
            for item in Lst2:
                if(item < "0" or item > "9") and (item != "#"):
                    Lst[int(buff)] = item
                    del Lst2[indexOf]
                    buff=""
                    break
                indexOf+=1
            del Lst2[i]
            indexOf=0
        elif Lst2[i]>="0" and Lst2[i]<="9":
            buff+=Lst2[i]
            del Lst2[i]
    #Deleting resources:
    del Lst2
    del buff
    #Getting the string back:
    Message=""
    while (i<len(Lst)):
        if(Lst[i]=="_"):
            Message+=" "
        else:
            Message+=Lst[i]
        i+=1
    return Message


Message = input("Enter a message: ")
print("The original message is: ", Message)
print("The decoded message is: ", DecodeMessage(Message))

#Keep the console opened until the next button pressed.
print()
input("Press any key to quit.")
