#Exercise: given a list of names, return another list cotaining only the 4-letters
#elements from that list.
def friend(x):
    #Code
    count_letters=0
    Lst=[]
    for word in x:
        for letter in word:
            count_letters+=1
        if count_letters==4:
            Lst.append(word)
        count_letters=0
    return Lst

Lst=["Ryan", "Adam", "Carl", "John", "Marcus", "Derek", "Hilton"];
print("The original list is: ", Lst)
print("The returned list is: ", friend(Lst))

#Keep the console opened until the next button pressed:
input("Enter anything to quit.")
