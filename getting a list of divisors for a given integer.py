#Getting a list with all the divisors of a integer number.
#Except the divisor 1, and the number itself if the only divisor is number itself
#Return a message containing that the number is prime.

def divisors(integer):
    Lst = []
    for n in range(2,integer):
        if integer%n==0:
            Lst.append(n)
    if(len(Lst)<1):
        return str(integer) + " is prime"
    return Lst

number = int(input("Enter a number: "))
print("The divisors of ", number, " are: ", divisors(number))

#Keep the console opened until the next button pressed.
input("Press any key to quit.")
