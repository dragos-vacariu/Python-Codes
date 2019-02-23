#Input and Output to files.

#If the file doesn't exists, then it will be created.
MyFile = open("dragos.txt", "w")

#"w" - Opens a file for writing only. Overwrites the file if the file exists.
#If the file does not exist, creates a new file for writing.

#"r" - Opens a file for reading only. The file pointer is placed at the beginning
#of the file. This is the default mode.

#"rb" - Opens a file for reading only in binary format. The file pointer is placed
#at the beginning of the file. This is the default mode.

#"rb+" - Opens a file for both reading and writing in binary format. The file
#pointer placed at the beginning of the file.

#"wb" - Opens a file for writing only in binary format. Overwrites the file if the
#file exists. If the file does not exist, creates a new file for writing.

#"w+" - Opens a file for both writing and reading. Overwrites the existing file if
#the file exists. If the file does not exist, creates a new file for reading
#and writing.

#"wb+" - Opens a file for both writing and reading in binary format. Overwrites
#the existing file if the file exists. If the file does not exist, creates a
#new file for reading and writing.

#"a" - 	Opens a file for appending. The file pointer is at the end of the file
#if the file exists. That is, the file is in the append mode. If the file does
#not exist, it creates a new file for writing.

#"ab" - Opens a file for appending in binary format. The file pointer is at the
#end of the file if the file exists. That is, the file is in the append mode.
#If the file does not exist, it creates a new file for writing.

#"a+" - Opens a file for both appending and reading. The file pointer is at the
#end of the file if the file exists. The file opens in the append mode. If the
#file does not exist, it creates a new file for reading and writing.

#"ab+" - Opens a file for both appending and reading in binary format. The file
#pointer is at the end of the file if the file exists. The file opens in the
#append mode. If the file does not exist, it creates a new file for reading
#and writing.

#The write() method writes any string to an open file. It is important to note that
#Python strings can have binary data and not just text.
#IMPORTANT - The write() method does not add a newline character ('\n')
MyFile.write("This program is written in Python language. By Program: 'files for inputting and outputting'")
#The string above will be written after the files gets closed (in the next line)
MyFile.close();
#The close() method of a file object flushes any unwritten information and closes
#the file object, after which no more writing can be done. Python automatically
#closes a file when the reference object of a file is reassigned to another file.
#It is a good practice to use the close() method to close a file.

MyFile = open("dragos.txt", "r")
Msg = MyFile.read(11) #Only the first 11 character will be extracted from the file.
print(Msg)
#IMPORTANT - when reading character from a file the cursor will move across the
#content of a file, so if it reaches the end, it will need to be reset using
#seek() function.

#The read() method reads a string from an open file. It is important to note that
#Python strings can have binary data. apart from text data.
Msg = MyFile.read(11) # This will print the next 11 character in the file
#since the cursor wasn't restarted.
print(Msg)
# Check current position
position = MyFile.tell();
print ("Current file position : {0}"  .format(position))
position = MyFile.seek(0, 0); #this will restart the cursor to the beginning of the file.
Msg = MyFile.read(11)
print(Msg)

#This function will rename a file:
import os #needed for the following function.
#Syntax: os.rename(current_file_name, new_file_name)

#Getting the current file name:
print("The current file name is: {0}" .format(MyFile.name))
#The attribute .name shows the name of the current file loaded.
MyFile.close() # without closing the file it won't work.
if os.path.isfile("dragos1.txt"): #checking if a file exists
    os.remove("dragos1.txt") #removing a file
os.rename("dragos.txt", "dragos1.txt")#renaming the file

#Renaming the file with the name of an existing file (at the same path) will
#throw an exception.

MyFile = open("dragos1.txt", "r")
print("The current file name is: {0}" .format(MyFile.name))
#Changing the name of the file will work only if the file is closed, and not being
#processed by another programs.

#Removing a directory:
os.chdir(r"C:\Users\Black2\Desktop\python") #Changing the current directory
if os.path.exists(r"C:\Users\Black2\Desktop\python\dragos dir"): #checking for a directory
    os.rmdir(r"C:\Users\Black2\Desktop\python\dragos dir") #removing directory

#Creating a directory:
os.mkdir("dragos dir")

#The os.getcwd() method displays the current working directory.
print("The current working directory is: {0}" .format(os.getcwd()))

#Renaming directories:
if os.path.exists(r"C:\Users\Black2\Desktop\python\dragos dir2"): #checking for a directory
    os.rmdir(r"C:\Users\Black2\Desktop\python\dragos dir2") #removing directory

os.rename(r"C:\Users\Black2\Desktop\python\dragos dir",
             r"C:\Users\Black2\Desktop\python\dragos dir2")#renaming the file

MyFile.close()
os.rmdir(r"C:\Users\Black2\Desktop\python\dragos dir2")
#The file Object Attributes
#file.closed	Returns true if file is closed, false otherwise.
#file.mode	Returns access mode with which file was opened.
#file.name	Returns name of the file.
#file.softspace	Returns false if space explicitly required with print, true otherwise.


#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
