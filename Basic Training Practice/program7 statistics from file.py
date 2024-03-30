#Somnoroase pasarele
#Statistici:
# -numar linii scrise
# -numar cuvinte
# -numar cuvinte unice (fara case)
# -numar

poezia = open("./resources/somnoroase_pasarele.txt", "r")
words = list()
lines = 0
frequecy_keeper = {}
characters = 0
print("Statistics: \n")

for line in poezia:
    aux=""
    for letter in line:
        if letter == " ":
            words.append(aux.capitalize()) #use same common case for all words
            aux=""
        elif letter >= 'a' and letter <= 'z' or (letter >='A' and letter <='Z'):
            aux+=letter
        characters+=1
    if aux != "":
        words.append(aux.capitalize()) #use same common case for all words
        aux = ""
    lines+=1
poezia.close()

word_unique = set(words)
for word in word_unique:
    frequecy_keeper[word] = words.count(word)

print("Number of lines: " + str(lines))
print("Number of words: " + str(len(words)))
print("Number of letters: " + str(characters))
print("Number of unique words: " + str(len(word_unique)) + "\n")
print(frequecy_keeper)

input("\nPress ENTER to exit.")