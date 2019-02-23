def FirstReverse(str): 
    revstr=""
    i=len(str)-1
    while(i>-1):
        revstr+=str[i]
        i-=1
    return revstr
    
# keep this function call here  
print (FirstReverse(input("Enter a string: ")))

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
