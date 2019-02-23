#This synthax of FOR loop works like FOREACH

for letter in 'Python':     # letter is the variable in which will be stored
#each element of the collection (String).
   print ("Current Letter : {0}" .format(letter)) #This will print the current letter

print("\n")
fruits = ['banana', 'apple',  'mango']
for fruit in fruits:
   print ("Current fruit : {0}" .format(fruit))


#This works as a normal FOR loop:
for num in range(10,20):  #to iterate between 10 to 20
    for i in range(2,num): #to iterate on the factors of the number
        if num%i == 0:      #this "if statement" is in the inner loop.
            j=num/i          #to calculate the second factor
            print ("{0} equals {1} * {2}"  .format(num,i,j))
            break #to move to the next number, the #first FOR
    else:                  # this "else statement" is in the outer loop
        print ("{0} is prime number" .format(num)) 

#While Loops
print("The following is WHILE loop:\n")
count = 0
while (count < 9):
   print ("The count is: {0}" .format(count))
   count = count + 1        

#Infinite While Loops
var = 1
while var == 1 :  # This constructs an infinite loop
   num = input("Enter a number  :")
   print ("You entered: {0}" .format(num))

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
