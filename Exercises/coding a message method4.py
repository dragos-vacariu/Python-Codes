def CodingMessage(Message, key):
    Lst = []
    Lst.append(str(key))
    #Converting string to list, and encoding:
    if(key+122 > 126):
        Lst.append("+#")
        for letter in Message:
            if letter!= " ":
                Lst.append(chr(ord(letter)-key))
            else:
                Lst.append(letter)
        Lst.append("#")
    else:
        Lst.append("-#")
        for letter in Message:
            if letter!= " ":
                Lst.append(chr(ord(letter)+key))
            else:
                Lst.append(letter)
        Lst.append("#")
    #Creating the string back:
    Message=""
    for item in Lst:
        Message+=item
    return Message





Message = input("Enter a message string: ")
key=11
while(key>10 or key<0):
    key = int(input("Enter a key (an integer number between 1 and 10):"))
print()
print("The coded message is: ", CodingMessage(Message, key))

#Keep the console opened until the next button pressed:
print()
input("Press any key to quit.")
