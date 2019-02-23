#Check for eureka numbers in interval.
#Eureka number is a number that can be composed from the sum of each of its digits
#raised at the power of the order appeared in the number.
#Example: 1 == 1**1
#         2 == 2**1
#         89 == 8**1 + 9**2
# WHERE ** MEANS RAISED TO POWER

def sum_dig_pow(a, b): # range(a, b + 1) will be studied by the function
    Lst = []
    Lst2 = []
    sum=0
    order=1
    for n in range (a, b+1):
        n1=n
        while(n>=1):
          Lst.append(n%10)
          n=int(n/10)
        i=len(Lst)-1
        while i>-1:
            sum += Lst[i] ** order
            order += 1
            i-=1
        if(sum==n1):
          Lst2.append(sum)
        sum=0
        Lst=[]
        order=1
    return Lst2

num = int(input("Enter a number: "))
print("The value returned is: " , sum_dig_pow(1, num))

#Keep the console opened until the next button pressed.
input("Press any key to continue: ")
