#Decimal to Hexadecimal converter:

def DecimalToHex(a):
    Lst=[];
    while(a>0):
        Lst.append(a&0b1111)
        a=a>>4
    hex=""
    i = len(Lst);
    while(i>0):
        i-=1
        hex+=str(GetHexDigit(Lst[i]))
    print("The hexa number is: {0}" .format(hex))

def GetHexDigit(a):
    if a is 10:
        return 'A'
    elif a is 11:
        return 'B'
    elif a is 12:
        return 'C'
    elif a is 13:
        return 'D'
    elif a is 14:
        return 'E'
    elif a is 15:
        return 'F'
    else:
        return str(a)

number = int(input("Enter a number: "))
DecimalToHex(number)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
