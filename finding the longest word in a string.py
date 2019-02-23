def LongestWord(sen): 
    longest=""
    currentLong=""
    for letter in sen:
        if letter is " ":
            if len(currentLong)>len(longest):
                longest = currentLong
            currentLong=""
        else:
            currentLong+=letter
    if len(currentLong)>len(longest):
        longest = currentLong
    return longest

def LongestWordOnlyLetters(sen): 

    # code goes here 
    longest=""
    currentLong=""
    for letter in sen:
        if (letter >= "A" and letter<="Z") or (letter >="a" and letter<="z"):
            currentLong+=letter
        else:
            if len(currentLong)>len(longest):
                longest = currentLong
            currentLong=""
    if len(currentLong)>len(longest):
        longest = currentLong
    return longest
# keep this function call here

Msg = input("Enter a sentence: ")
print (LongestWord(Msg))
print (LongestWordOnlyLetters(Msg))


#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
