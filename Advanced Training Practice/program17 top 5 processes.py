import os

f = os.popen("tasklist", "r") # getting a list of task currently running on Windows.

data = []
for line in f.readlines():
    data.append(line)

data = data[3:]
f.close()


print("*" * 30)

class Process:
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory
    def __repr__(self):
        return self.name + " => " + str(self.memory) + " Bytes"


processList = []

for line in data:
    factor = len(line)-len("============")
    aux = "".join(line[factor:])
    memory = aux.replace(" ", "")
    memory = memory.replace(",", ".")
    memory = memory.replace("\n", "")
    if "K" in memory:
        memory = float("".join(memory[:len(memory)-2]))*1024
    elif "M" in memory:
        memory = float("".join(memory[:len(memory) - 2])) * 1024**2
    elif "G" in memory:
        memory = float("".join(memory[:len(memory) - 2])) * 1024**3
    obj = Process(line[:len(line)-len("============")], memory)
    processList.append(obj)

processList = sorted(processList, key= lambda x: x.memory, reverse=True)

print("TOP 5: \n")

for x in range(0, 5):
    print(processList[x])

