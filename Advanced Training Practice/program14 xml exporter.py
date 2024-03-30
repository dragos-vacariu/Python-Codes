import os

import sys
import xml.etree.ElementTree

class Persoana:
    def __init__(self, nume:str, prenume:str, varsta: int):
        self.nume = nume
        self.varsta = varsta
        self.prenume = prenume

    def __repr__(self):
        return self.nume+ " " + self.prenume + " " + str(self.varsta)

persoane = [
                Persoana("Geere", "Richard", 64),
                Persoana("Walker", "Alan", 24),
                Persoana("Manson", "Mary", 34),
                Persoana("Manson", "Deny", 36),
                Persoana("Menance", "Denise", 54),
                Persoana("Reyes", "Antonio", 22),
            ]

def write_xml(lista, filename):
    root  = xml.etree.ElementTree.Element("Persoane")
    for pers in lista:
        node = xml.etree.ElementTree.Element("persoana", varsta = str(pers.varsta))
        nume = xml.etree.ElementTree.SubElement(node, 'nume')
        prenume = xml.etree.ElementTree.SubElement(node, 'prenume')
        nume.text = pers.nume
        prenume.text = pers.prenume
        root.append(node)
    tree = xml.etree.ElementTree.ElementTree(root)
    try:
        tree.write(filename, "UTF-8")
    except EnvironmentError as err:
        print("{0}: import error: {1}".format(
            os.path.basename(sys.argv[0]), err))
        return False
    return True

def read_xml(filename):
    try:
        tree = xml.etree.ElementTree.parse(filename)
    except Exception as err:
        print(err)
        return
    result = []
    root = tree.getroot() # return the root of the xml file
    nodeList = root.findall('persoana') # return a list of nodes with specified name
    for node in nodeList:
        varsta = int(node.get('varsta'))
        nume = node.find('nume').text
        prenume = node.find('prenume').text
        result.append(Persoana(nume, prenume, varsta))
    return result

write_xml(persoane, "fisier.xml")

obj = read_xml("fisier.xml")

print(obj)
