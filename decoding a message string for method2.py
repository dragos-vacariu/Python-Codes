def Decoder(Message):
    Lst = []
    Lst2 = []
    i=0
    buf=""
    key=0;
    #Separating string in list:
    while(i<len(Message)):
        buf+=Message[i]
        if (ord(Message[i])<48 or ord(Message[i])>57):
            Lst.append(buf)
            buf=""
        Lst2.append(" ") #initializing second list
        i+=1
    #Discovering the "key" and deleting "{" at the beginning and ending "}".
    for item in Lst:
        for symbol in item:
            if symbol is "{":
                key=int(buf)
            else:
                buf+=symbol
    del Lst[0]
    del Lst[len(Lst)-1]
    #Decoding the string:
    buf=""
    for item in Lst:
        for symbol in item:
            if(ord(symbol) >=48 and ord(symbol)<=57):
                buf+=symbol
            else:
                temp=int(buf)
                if(temp>key):
                    Lst2[temp-key]=symbol
                else:
                    Lst2[key-temp]=symbol
        buf=""
    Message=""
    #Creating the string back:
    for item in Lst2:
        if(item=="_"):
            Message+=" "
        else:
            Message+=item
    return Message

Message = input("Enter a message: ")
print("The original message is: ", Message)
print("The decoded message is: ", Decoder(Message))

#Keep the console opened until the next button pressed.
print()
input("Press anything to quit.")
