#This is a module (a module can be any .py file):


#These are the functions:
def print_func( par ):
   print ("Hello : {0} " .format(par))
   return

def CalculateSum (*Args):
    sum=0
    for item in Args:
        sum+=item
    return sum
