#Return the sum of all the numbers between a and b, including them.
def get_sum(a,b):
    #good luck!
    sum=0
    if a==b:
        return a
    elif a>b:
        for number in range(b,a):
            sum+=number;
            print("Sum = ", sum)
        sum+=a
    else:
        for number in range(a,b):
            sum+=number;
            print("Sum = ", sum)
        sum+=b
    return sum;


number1 = int(input("Enter number1: "))
number2 = int(input("Enter number2: "))
result = get_sum(number1, number2)
print("The result is : " , result)

#Keep the console opened until the next button pressed.
input("Press any key to continue...")
