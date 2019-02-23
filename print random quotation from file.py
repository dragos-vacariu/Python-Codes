#This program will print a random quotes from the .txt quotation file opened below. 
from random import randint

def ReadFromFile():
    MyFile = open(r"D:\my files\quotations.txt", "r")
    Line=MyFile.read(1000000)
    i=0
    numberOfQuotes=0
    MyList=[]
    buff=""
    while(i<len(Line)):
        if(Line[i]=="\n"):
            MyList.append(buff)
            buff=""
            numberOfQuotes+=1
        else:
            buff+=Line[i]
        i+=1
    #Getting a random number between 0 and numberOfQuotes
    choice = randint(0,numberOfQuotes)
    #Printing the choice:
    print(MyList[choice])

#Calling the function:
while(input("Press C to continue, or Q to quit: ")=="C"):
    print()
    ReadFromFile()
    print()

#Keep the console opened until the next button pressed:
input("Press any key to quit.")
