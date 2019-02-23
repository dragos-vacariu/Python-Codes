'''
Exercise: determine if it is an acceptable sequence by either returning the
string true or false. The str parameter will be composed of + and = symbols
with several letters between them (example: "++d+===+c++==a") and for the string
to be true each letter must be surrounded by "+" symbols.  The string will not
be empty and will have at least one.
letter.
'''
def SimpleSymbols(str): 
    # code goes here 
    i=0
    status="false"
    if len(str) < 1 :
        return False
    while(i < len(str) ):
        if (str[i]>="a" and str[i]<="z") or (str[i]>="A" and str[i]<="Z"):
            if i>0 and str[i-1] == "+" and i<(len(str)-1) and str[i+1] =="+":
                status = "true"
                i+=1
                continue
            else:
                return "false"
        i+=1
    
    return status
    
# keep this function call here  
print (SimpleSymbols(input("Enter a string: ")))

#Keep the console opened for the next button pressed:
input("Press any key to quit.")
