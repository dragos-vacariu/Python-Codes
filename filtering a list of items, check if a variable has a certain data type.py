#Exercise the function below will take a list as an argument, and it will return
#back a list whom's items will be only the int's from the passed argument.
#IF none then it will return an empty list.

def filter_list(l):
    filtered = []
    for letter in l:
        if isinstance(letter, int):
            filtered.append(letter)
    return filtered

List=[103,44,55,'ABC', "c", 2]
print("The original list is: " + str(List))
print("The filtered list is: " + str(filter_list(List)))

#Keep the console opened until the next button pressed.
input("Press any key to quit. ")
