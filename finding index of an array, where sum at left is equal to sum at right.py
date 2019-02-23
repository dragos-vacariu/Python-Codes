#Finding the index of the element which have the sum_left == sum_right:
def find_even_index(arr):
    #your code here
    sum_left=0
    sum_right=0
    i=0
    while(i<len(arr)):
        for num in range(0,i):
            sum_left+=arr[num]
        for numb in range(i+1,len(arr)):
            sum_right+=arr[numb]
        print("Iteration : ", i, " sum_left: ", sum_left, " sum_right", sum_right)
        if sum_left==sum_right:
            return i
        else:
            sum_left=0
            sum_right=0
        i+=1
    return -1

arr = [1,2,3,4,3,2,1]
print("The index is: ", find_even_index(arr))

#Keep the console opened until the next button pressed:
input("Press any key to quit.")
