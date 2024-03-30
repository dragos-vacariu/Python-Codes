import sys

if __name__ == "__main__": #if script is run from this file do this, otherwise it means file imported by other module and you will ignore this.
    if len(sys.argv) > 1: #there is always gonna be at least one element in this... at index 0 the name of the file is stored.
        print ("The script has the name "  + str(sys.argv[0]))
        print ("The arguments which were passed are: " + str(sys.argv[1:]))