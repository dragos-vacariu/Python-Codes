#Exercise: check if the given argument can be achieved by summing a cube of terms
# greater than 0 and below its value.
# m = number to be checked.
# n = the last value of the cubic sum
#Example:
#m=45
#Can be 45 achieved using a sum from 1**3+2**3 + ....
#if so: n will be the last base raised to the cubic power.
#else: there is no such n.
#
#So if there is a series of 4-5 terms whom cubic sum is greater than 45, there
#will be no such n.
def find_nb(m):
    # your code
    sum = 0
    n = 1
    while (sum < m):
        sum += n**3
        n +=1
    if sum == m:
        return (n-1)
    else:
        return (-1)
number=int(input("Enter a number: "))
number=find_nb(number)
if number is -1:
    print("There is not such an n!")
else:
    print("n has the value: ", number)

#Keep the console opened for the next button pressed.
input("Press any key to quit.")
