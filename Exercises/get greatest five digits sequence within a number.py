#Exercise: In the following 6 digit number -> 91 is the greatest sequence
#of 2 digits.
#Write a program to obtain the greatest 5 digits sequence, from a given only-digits
#string.

def solution(digits):
    digits=int(digits)
    Nmbs = []
    while digits>0:
        Nmbs.append(digits%100000)
        digits=int(digits/10)
    greatest=Nmbs[0]
    for numbs in Nmbs:
        if numbs>greatest:
            greatest=numbs
    return greatest;

number = int(input("Enter a number: "))
print("The greatest sequence is: ", solution(number))

#Keep the console opened until the next button pressed.
input("Press any key to quit. ")
