def LetterCapitalize(str): 
    # code goes here
    i=0
    str2=""
    while(i<len(str)):
        if i>0 and str[i-1] is " " and str[i]>="a" and str[i]<="z":
            str2+=str[i].upper()
        elif i == 0:
            str2+=str[i].upper()
        else:
            str2+=str[i]
        i+=1
    return str2
    
# keep this function call here  
print (LetterCapitalize(input("Enter a sentence: ")))

#Keep the console open until the next button press:
input("Press any key to quit.")
