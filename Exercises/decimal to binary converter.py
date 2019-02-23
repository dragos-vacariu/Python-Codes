#Decimal to binary converter:

#Creating a function
def ConvertToHex(a):
    Lst=[]; #creating an empty list
    while(a>0):
        Lst.append(a&0b1) # appending each bit of the number to the list
        a=a>>1 #shift the copied bit out from the number
    size = len(Lst) #get the size of the list
    bin = ""
    while(size>0):
        bin+= str(Lst[size-1]) # append the bit to the string
        del Lst[size-1] #delete the element in the list
        size = len(Lst) #get the size of the list
    print("The binary number is: {0}" .format(bin)) #print the result

#Program starts here
Number=int(input("Enter a number: "))
ConvertToHex(Number)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
