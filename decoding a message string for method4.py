def DecodingMessage(Message):
    Lst = []
    buff = ""
    key = 0
    indexCounter=0
    #Converting string into list:
    for item in Message:
        Lst.append(item)
    #Getting the key and operation:
    while indexCounter<len(Lst):
        if Lst[indexCounter] < "0" or Lst[indexCounter] > "9":
            key = int(buff)
            buff=Lst[indexCounter]
            del Lst[indexCounter]
            break
        buff+=Lst[indexCounter]
        del Lst[indexCounter]
    #Deleting resources:
    del indexCounter
    del Lst[0]
    del Lst[len(Lst)-1]
    #Converting List to string and decoding:
    Message=""
    if(buff=="+"):
        for item in Lst:
            if item!= " ":
                Message+=chr(ord(item)+key)
            else:
                Message+=" "
    else:
        for item in Lst:
            if item!= " ":
                Message+=chr(ord(item)-key)
            else:
                Message+=" "
    return Message

Message = input("Enter a message string: ")
print()
print("The decoded message is: ", DecodingMessage(Message))

#Keep the console opened until the next button pressed:
print()
input("Press any key to quit.")
