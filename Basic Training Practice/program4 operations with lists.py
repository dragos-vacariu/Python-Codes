import random
import pickle

#Lista de string-uri
#Meniu
#Optiunea 1: Adauga element
#Optiunea 2: Sorteaza crescator
#Optiunea 3: Sorteaza descrescator
#Optiunea 4: Sterge element ? if not found: element nu e in lista
#Optiunea 5: Amesteca / Shuffle
#Optiunea 6: Afiseaza
#Optiunea 7: Iesire

def ShowMenu():
    print("\nMENIU\n")
    print("Optiunea #0: Genereaza lista")
    print("Optiunea #1: Adauga element")
    print("Optiunea #2: Sorteaza crescator")
    print("Optiunea #3: Sorteaza descrescator")
    print("Optiunea #4: Sterge element")
    print("Optiunea #5: Amestecare")
    print("Optiunea #6: Afiseaza")
    print("Optiunea #7: Salvare fisier text")
    print("Optiunea #8: Restaureaza fisier text")
    print("Optiunea #9: Salvare fisier binar")
    print("Optiunea #10: Restaureaza fisier binar")
    print("Optiunea #11: Iesire")

def RemoveElem():
    removeElem = "None"
    while (removeElem == "None"):
        removeElem = int(input("Alegeti element: "))
        if removeElem < 0 or removeElem >= len(elements):
            print("Element invalid")
            removeElem = "None"
    return removeElem

def GenerateList(x):
    numberofItems = int(input("How many items? "))
    while numberofItems :
        x.append(random.randint(0,100))
        numberofItems-=1

def saveFile(option="text"):
    if(option=="binary"):
        my_file = open("file_program4.bin", "wb")
        pickle.dump(elements, my_file)
    else:
        my_file = open("file_program4.txt", "w", encoding="utf-8")
        for element in elements:
            my_file.write(str(element) + "\n")
    my_file.close()

userChoice = 12
elements = list()


while(userChoice != 9 ):
    ShowMenu()
    userChoice = int(input("\nAlegeti optiunea: "))
    if userChoice == 0:
        GenerateList(elements)
    elif userChoice == 1:
        elements.append(input("Introduceti element: "))
    elif userChoice == 2:
        elements.sort()
    elif userChoice == 3:
        elements.sort(reverse=True)
    elif userChoice == 4:
        del elements[RemoveElem()]
    elif userChoice == 5:
        random.shuffle(elements)
    elif userChoice == 6:
        print(elements)
    elif userChoice == 7 :
        saveFile()
        print("Salvare completa")
    elif userChoice == 8 :
        my_file = open("file_program4.txt", "r", encoding="utf-8")
        elements = list()
        for line in my_file:
            elements.append(line.replace("\n",""))
        my_file.close()
        print("Restaurare completa")
    elif userChoice == 9:
        saveFile("binary")
        print("Salvare binara completa")
    elif userChoice ==10:
        my_file = open("file_program4.bin", "rb")
        elements = pickle.load(my_file)
        my_file.close()
        print("Restaurare binara completa")
    elif userChoice == 11 :
        my_file = open("file_program4.txt", "r", encoding="utf-8")
        saved_file = my_file.read().split()
        if saved_file != elements:
            print("Vrei sa salvezi?")
            ans = input("Y/N : ")
            if(ans.capitalize() == "Y"):
                saveFile()
                print("Salvare completa")
    elif userChoice > 11 :
        print("Optiune inexistenta")
