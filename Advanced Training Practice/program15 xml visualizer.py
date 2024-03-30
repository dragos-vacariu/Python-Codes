import xml.etree.ElementTree

class Persoana:
    def __init__(self, nume:str, prenume:str, varsta: int):
        self.nume = nume
        self.varsta = varsta
        self.prenume = prenume

def read_xml(filename):
    message = ""
    try:
        tree = xml.etree.ElementTree.parse(filename)
    except Exception as err:
        print(err)
        return
    root = tree.getroot() # return the root of the xml file
    message += str(root).split("'")[1] + "\n"
    for node in root:
        message += "\t"+str(node).split("'")[1] + "\n"
        if node.attrib != {}:
            message += "\t\t"
            for x in range(0, len(node.attrib.keys())):
                message+= str(list(node.attrib.keys())[x]) + " = " +str(list(node.attrib.values())[x]) + "\n"
        for element in node:
            elementTag = str(element).split("'")[1]
            message += "\t\t\t"+elementTag + "\n"
            if element.attrib != {}:
                message += "\t\t\t\t"
                for x in range(0, len(element.attrib.keys())):
                    message += str(list(element.attrib.keys())[x]) + " = " + str(list(element.attrib.values())[x]) + "\n"
            if element.text!="":
                message += "\t\t\t\t\t" + element.text + "\n"
    message += str(root).split("'")[1] + "\n"
    print(message)

read_xml("fisier.xml")
input("Press any RETURN to exit.")