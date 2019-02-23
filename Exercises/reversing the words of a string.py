#Exercise reversing the words of a string sentence.

def reverseWords(str):
    NewStr=""
    word = ""
    i=len(str)-1
    while i > -1:
        if(str[i] == " "):
            j=len(word)-1
            while(j>-1):
                NewStr+= word[j]
                j-=1
            NewStr += " "
            word = ""
        else:
            word+=str[i]
        i-=1
    i=len(word)-1
    while(i>-1):
        NewStr+=word[i]
        i-=1
    return NewStr

strng = input("Enter a string: ")
print("The string is: ", reverseWords(strng))

#Keep the console opened until the next button pressed.
input("Press any key to quit: ")
