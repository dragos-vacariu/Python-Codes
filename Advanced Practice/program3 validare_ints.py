class Validare:
    def __call__(fct, *args):
        def proxy(*args):
            for x in range(0,len(args)):
                if type(args[x]) != int:
                    print(str(args[x])+ " - Argument number: " + str(x) + " is not of integer type.")
                    try: raise Exception
                    except Exception:
                        print("Argument not of Integer Type.")
            else:
                fct(*args)
        return proxy

valideaza_ints = Validare() #this is a functor
@valideaza_ints #this is a functor
def f(a,b,c): pass

@valideaza_ints
def g(val):pass


f(4,1,9) #OK
f(4,'casa',55) #NOT OK, param 2 nu e ok.
g('x')
