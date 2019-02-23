'''Exercise changing the each consonant letter in a string with the following
alphabetic one example a -> b , z -> a, h -> i ....
If letter is lowercase vowel, then uppercase it
Example: a->A , i->I , o->O , u->U , e->E.
'''

def LetterChanges(str1): 
    SetO = {"a", "e", "i", "o", "u"}
    # code goes here 
    str2=""
    for letter in str1:
        if(letter>='A' and letter <= 'Z') or (letter >= 'a' and letter <='z'):
            if letter in SetO:
                str2+= letter.upper()
            else:
                str2+= chr(ord(letter)+1)
        else:
            str2+=letter
    return str2
    
# keep this function call here  
print (LetterChanges(input("Enter a string: ")))

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
