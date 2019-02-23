def Decoder(Message):
    Lst = []
    Lst2 = []
    i=0
    buf=""
    #Separating string in list:
    while(i<len(Message)):
        buf+=Message[i]
        if (ord(Message[i])<48 or ord(Message[i])>57):
            Lst.append(buf)
            buf=""
        Lst2.append(" ") #initializing second list
        i+=1
    #Decoding the string:
    buf=""
    for item in Lst:
        for symbol in item:
            if(ord(symbol) >=48 and ord(symbol)<=57):
                buf+=symbol
            else:
                Lst2[int(buf)-1]=symbol
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
