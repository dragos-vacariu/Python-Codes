#Write a function, persistence, that takes in a positive parameter num and returns
#its multiplicative persistence, which is the number of times you must multiply
#the digits in num until you reach a single digit.

def persistence(n):
    # your code
    product=100
    numberOfTimes=0
    if n<10:
        return 0
    while(product>9):
        product=n
        Digits = []
        while(product):
            Digits.append(product%10)
            product=int(product/10)
        product=1
        print(Digits)
        for num in Digits:
            product*=num
        numberOfTimes+=1
        n=product
    return numberOfTimes

number = int(input("Enter a number: "))
print("Times : ",  persistence(number))

#Keep the console opened until the next button pressed:
input("Press any key to quit.")
