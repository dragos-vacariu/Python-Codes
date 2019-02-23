Dict = { "GOOGLE": 53.22, "FACEBOOK": 77.22, "TUMBLR": 33.2}

#Splitting dictionary to lists:
#Dict.values() => this will return a list with all the values in dictionary
#Dict.keys() => this will return a list with all the keys in the dictionary

#Zipping a dictionary:
name = zip(Dict.values(), Dict.keys())

#The zipped dictionary will look like this:
#(33.2, 'TUMBLR'), (53.22, 'GOOGLE'), (77.22, 'FACEBOOK')
#The same would be in case of lists, 1->1, 2->2
#first element combined with first, second to second... etc

print("The original dictionary is: ", Dict)
#Sorting a zipped dictionary:
print("The sorted(by value) zipped dictionary is: ", sorted(name))

name = name = zip(Dict.keys(), Dict.values())
print("The sorted (by keys) zipped dictionary is: ", sorted(name))
