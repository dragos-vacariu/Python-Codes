
import time

def masoara_timp(fct):
    if hasattr(fct, 'call_number') == False:
        fct.call_number = 1
        fct.call_time = 0
    print("Apel decorator.")
    def proxy():
        print("Apel proxy.")
        t = time.time()
        fct()
        fct.call_time += time.time() - t
        print("Functia " + str(fct.__name__) + " : s-a executat in : " + str(time.time() - t))
        print("Apeluri functie " + str(fct.call_number))
        print("Durata medie: " + str(fct.call_time / fct.call_number))
        fct.call_number += 1
    return proxy


#masoara_timp este un decorator. Un decorator este un callable ce primeste un callable si returneaza un callable.
#Un decorator este un callable cu functii.
@masoara_timp #this is equivalent to functie = masoara_timp(functie)
def functie():
    time.sleep(0.5)
    print("se executa functia")

functie()
functie()
functie()
functie()
functie()


