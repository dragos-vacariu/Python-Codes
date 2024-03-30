#Context manager are objects which can use "with expression as variable". Example files.
#with open("file.txt", "rt") as file -> where open is a constructor of a class belonging to Context Manager.

class CM:
    #Creating a context manager class.
    def __init__(self):
        print("Constructor called.")
    def __enter__(self):
        print("Enter function.")
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Exit function. " + str(exc_tb) + " " + str(exc_type) + " " + str(exc_value))

        #when returning True from the __exit__ the exception is not allowed to leave the function.
        #The exception gets hidden/handled in the __exit__

try:
    with CM():
        print("Action")
        raise Exception ("Problem.")
        print("Action stop.")
except Exception:
    print("Exception occured.")
input("Press any RETURN to exit.")