# exercitiu,
#   python grap.py
#       casa -> c:\\hyp
#           sa se caute in directoare... un fisier ce contine cuvant:
#               sa raporteze: am gasit in fisier. txt la linia.... x... cuvantul... ex: casat....

import os
from multiprocessing import Process, Queue

def findMatch(content,word,file):
    for line in content:
        if word.upper() in line.upper():
            message = word + " was found on line: " + str(content.index(line) + 1) + " in file: " + str(
                file) + " within: "
            restOfLine = line.upper()[line.upper().find(word.upper()):]
            for letter in restOfLine:
                if letter == " ":
                    break
                message += letter
            print(message)

def searchWordInFileDirs(dir, word): #this function is called when loading a directory.
    for root, dirs, files in os.walk(dir):
        for file in files:
            fileContent = open(root + "/" + file, "rt")
            content = fileContent.readlines()
            fileContent.close()
            findMatch(content,word,file)


searchWordInFileDirs(r"./", "import")
input("Press any RETURN to exit.")