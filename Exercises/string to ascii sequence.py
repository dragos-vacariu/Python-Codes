#String to ASCII sequence.

def StrToInt(Msg):
    String=""
    for letter in Msg:
        String += str(ord(letter))
        String += " "
    print("The string in ASCII is: {0}" .format(String))
Message = input("Enter a string: ")
StrToInt(Message)

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
