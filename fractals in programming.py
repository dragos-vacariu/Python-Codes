#Fractals: dividing an interval into 3 intervals recursively, taking into account
#that 1 interval is printable the next one is not. If the interval above the current
#interval is not printable, the current one cannot also be printable.

#Exercise regarding fractals:
def Fractal(number):
    strng = ""
    rund=0
    while(getAnswer(2, number, rund)):
        rund+=1
        for n in range(1, number+1):
            if(getAnswer(n, number, rund)):
                strng+="#"
            else:
                strng+=" "
        strng+="\n"
    return strng
def getAnswer(n, number, rund):
    factor=3
    it=2
    for numb in range(1,rund):
        if(n>number/factor and n<=(number/factor*it)) or (n<=number-number/factor and n>number-(number/factor*it)) :
            it*=2
            return False
        factor*=3
    return True

number = int(input("Enter a number: "))
print(Fractal(number))

#Keep the console opened until the next button pressed:
input ("Press any key to quit.")
