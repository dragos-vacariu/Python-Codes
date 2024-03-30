import os

print("Enter a directory filepath: ")
filepath = str(input("filepath: "))

if os.path.exists(filepath):
   total_size = 0
   number_of_files = 0
   for dirs in os.walk(filepath):
       for subdirs in dirs:
           for files in subdirs:
               if os.path.isfile(files):
                   total_size+=os.path.getsize(files)
                   number_of_files += 1
   print("Directory size: " + str(total_size) + " bytes")
   print("Number of files: " + str(number_of_files))
else:
    print("Wrong filepath was entered.")

input("\nPress ENTER to exit.")