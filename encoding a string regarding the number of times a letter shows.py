def duplicate_encode(word):
    i=0
    string_new=""
    count_letter=0
    while(i<len(word)):
        for letter in word:
            if word[i] == letter.upper() or word[i] == letter:
                count_letter+=1
        if count_letter>1:
            string_new+=")"
        else:
            string_new+="("
        i+=1
        count_letter=0
    return string_new

word=input("Enter a string: ")
print("The encoded string is: ", duplicate_encode(word))

#Keep the console opened until the next button pressed:
input("Enter anything to quit.")
