import multiprocessing # used for multiprocessing
import time # used for time

def PrintHello():
    i=0
    while(i<50):
        print("Hello " + str(i))
        time.sleep(0.2)
        i+=1
def PrintHi():
    i=0
    while(i<50):
        print("Hi " + str(i))
        time.sleep(0.2)
        i+=1
def Funct(n): # functions used with ".pool and .map" needs to take an extra argument
    i=0
    while(i<50):
        print("Hello " + str(i))
        time.sleep(0.2)
        i+=1
        
if __name__ == "__main__":
    t_before = time.time()
    p1 = multiprocessing.Process(target=PrintHello, args=())
    p2 = multiprocessing.Process(target=PrintHi, args=())
    p1.start()
    p2.start()
    p1.join() # wait for the process to finish
    p2.join() # wait for the process to finish
    t_after = time.time()
    print("Example1. Time for execution: " + str(t_after - t_before))
#Executing single process:
    t_before = time.time()
    p1 = multiprocessing.Process(target=PrintHello, args=())
    p1.start()
    p1.join() # wait for the process to finish
    t_after = time.time()
    print("Example2. Time for execution: " + str(t_after - t_before))
#Pooling and mapping processes:
# Functions used for "pooling and mapping" needs to take an extra argument for
#iteration (how many times to run the same function).
    t_before = time.time()
    p1 = multiprocessing.Pool()
    p1.map(Funct, range(1)) # run this function for 1 time.
#The extra argument specifies how many times the function should be runned.
    t_after = time.time()
    print("Example2 with Pooling and Mapping. Time for execution: " + str(t_after - t_before))
#Keep the console open until the next button pressed:
    input("Press any key to quit.")

'''Multi processing does almost the same thing as multi-threading: it is used
for speeding up the execution of tasks, by executing them simultaneosly (in parallel).

SIMILARITIES:
Both multi-processing and multi-threading are used to speed up the execution of multiple
tasks (the both execute individual multi-tasking in parallel).

THE DIFFERENCES:
Each process has its own memory address space (stack memory): so when returning a value
from a process, the value returned will not be seen by the rest of the program
unless it is saved in a file, in a shared memory address, or in a message pipe.
Whereas threading is able to return values which can be used later in the main program.

A process is treated as an individual program, (it even creates a process in the
task mananger),

Processes can be sent through different cores, that would speed up the program even more.

Creating multiple processes is costly compare to threads. Since for each process
there is allocated another stack memory space.

ADVANTAGES FOR USING MULTI_PROCESSING (instead of multi-threading):

Separate memory space
Code is usually straightforward
Takes advantage of multiple CPUs & cores
Avoids GIL limitations for cPython
Eliminates most needs for synchronization primitives unless if you use shared memory (instead, it's more of a communication model for IPC)
Child processes are interruptible/killable
Python multiprocessing module includes useful abstractions with an interface much like threading.Thread
A must with cPython for CPU-bound processing

DISADVANTAGES FOR USING MULTI_PROCESSING:

IPC a little more complicated with more overhead (communication model vs. shared memory/objects)
Larger memory footprint'''
