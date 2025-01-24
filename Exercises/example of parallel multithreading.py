import os, time, threading

class Worker(threading.Thread):
    def __init__(self, nume):
        super().__init__(name=nume)

    def run(self):
        #This function is called when starting the thread
        print("start " + str(self.name))
        for value in range(0, 100000):
            print(self.name + " - " +  str(value))


def main():

    no_workers = 2
    worker_one = Worker("W"+str(1))
    worker_two = Worker("W"+str(2))
    #both will start
    worker_one.start()
    worker_two.start()
    #both will join work together
    worker_one.join()
    worker_two.join()

t0 = time.time()
main()
t1 = time.time()
print("\nTime taken:" + str(t1-t0) + " seconds.")