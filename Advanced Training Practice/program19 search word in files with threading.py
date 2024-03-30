import os, time, threading

class Queue:
    def __init__(self):
        self.lista = []
        self.mtx = threading.Lock()
    def put(self, val):
        with self.mtx:
            self.lista.append(val)
    def get(self):
        with self.mtx:
            return self.lista.pop(0)

class Worker(threading.Thread):
    def __init__(self, nume, names, searched):
        super().__init__(name=nume)
        self.names = names
        self.searched = searched
    def run(self):
        #print("start " + str(self.name))
        while True:
            try:
                file = self.names.get()
            except:
                break
            self.process(file, self.searched)
        #print("stop "  + str(self.name))

    def process(self, filename, word):
        try:
            with open(filename) as f:
                # with open(f'{root}/{file}') as f:
                file_printed = True
                for line_count, line in enumerate(f, 1):
                    if word in line:
                        if file_printed:
                            print(filename)
                            file_printed = False
                        print("Line " + str(line_count) + ": " + str(line.strip()))
        except:
            pass


def main(directory, searched):
    names = Queue()
    counter = 0
    # 1. produc informatia
    for root, dirs, files in os.walk(directory):
        counter += len(files)
        for file in files:
            filename = os.path.join(root, file)
            names.put(filename)
    print("Total " + str(counter) + " files.\n")

    no_workers = 100
    workers = [Worker("W"+str(i), names, searched) for i in range(no_workers)]
    [w.start() for w in workers]
    [w.join() for w in workers]



t0 = time.time()
main(r"./", "import")
t1 = time.time()
print("\nTime:" + str(t1-t0) + " seconds.")
input("\nPress any RETURN to exit.")