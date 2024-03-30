#functie generator si expresie generator

def genereaza(s:str):
    for x in range(0, len(s)):
        s = s[x:] + s[0:x]
        yield s #return a value but without intrerrupting the function or the loop

print("Function:")
for s in genereaza("casa"):
    print(s)

print("\nExpresion:")
st = "casa"
for s in (st[x:] +st[0:x] for x in range(0,len(st))):
    print(s)

'''Output: casa, asac, saca, acas'''
input("Press any RETURN to exit.")