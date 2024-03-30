import pickle # for binary files

with open("binary_file.bin", "wb") as myFile: #when opening files using with, they will close automatically at the end of the block
    list_of_data = ["Ana", "are", "mere"]
    set_of_data = {"aa", "bb"}
    pickle.dump(list_of_data, myFile) # write to binary file
    pickle.dump(set_of_data, myFile) # write to binary file

with open("binary_file.bin", "rb") as myFile2:
    print("Read from binary file: " + str(pickle.load(myFile2))) #it will read the first item written
    print("Read from binary file: " + str(pickle.load(myFile2))) #it will read the second item written