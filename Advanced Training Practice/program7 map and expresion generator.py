#list comprehension

lst = [x*2 for x in range(0, 10)]
print(lst)

#expresie generator
xst = (x*2 for x in range(0, 10))
print(xst)

#expresion generator to list
l = list(xst)
print(l)

#using map
mapxp = map(lambda x: x**2, [2,3,4,5])
print(mapxp)