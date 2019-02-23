import threading #used for threading
import time #used for time

def calculateSquare(numberList):
    for n in numberList:
        print(str(n) + " * " + str(n) + " = " + str(n*n))
        time.sleep(0.2) #this will add a 0.2 seconds delay

def calculateCube(numberList):
    for n in numberList:
        print(str(n) + " * " + str(n) + " * " + str(n) + " = " + str(n*n*n))
        time.sleep(0.2) #this will add a 0.2 seconds delay

numberList = [2,4,5,6,12,34]
#Creating threads:
thread1 = threading.Thread(target=calculateSquare, args =(numberList,))
thread2 = threading.Thread(target=calculateCube, args =(numberList,))

t_before = time.time() # this will get the time before starting the threads
calculateSquare(numberList)
calculateCube(numberList)
t_after = time.time()
print("Example1 (without threading): Time for execution: " + str(t_after-t_before) + " seconds.")
print()

#THIS THREAD EXAMPLE WORKS AS CALLING THE 2 FUNCTIONS WITHOUT THREADING (just like in the example above):
#because the second thread needs to wait until the first thread finishes its execution.
#just like the functions in the example above do.
#Get current time:
t1_before = time.time() # this will get the time before starting the threads
thread1.start()
thread1.join() #wait for the thread1 to finish its work.
thread2.start()
thread2.join() #wait for the thread2 to finish its work.
t1_after = time.time()
print("Example2 (inefficient threading) : Time for execution: " + str(t1_after-t1_before) + " seconds.")
print()

#THIS WAY IS FASTER BUT PRINTING IS A MESS (BECAUSE THE 2 FUNCTIONS EXECUTE SIMULTANEOUS):
#After finishing, the thread needs to be reinitialized.
thread1 = threading.Thread(target=calculateSquare, args =(numberList,))
thread2 = threading.Thread(target=calculateCube, args =(numberList,))
t2_before = time.time() # this will get the time before starting the threads
thread1.start()
thread2.start()
thread1.join() #wait for the thread1 to finish its work.
thread2.join() #wait for the thread2 to finish its work.
t2_after = time.time()
print("Example3 (good threading) : Time for execution: " + str(t2_after-t2_before) + " seconds.")

#INFORMATION:
'''Multi-Threading - is the action of executing tasks simultaneosly (in parallel)
in order to increase the speed of execution.

COMPARISON BETWEEN MULTI_THREADING AND MUTI_PROCESSING:

Multi-threading shares the same stack memory as the whole program (this is one main difference comparing to multi-processing)
Multi-threading returns a value to the same memory address (stack address) whereas the multi-processing doesn't because
it's has it's own stack memory (in which it will copy all the variables related to it).

ADVANTAGES FOR USING MULTI_THREADING (instead of multi-processing):
Lightweight - low memory footprint
Shared memory - makes access to state from another context easier
Allows you to easily make responsive UIs
cPython C extension modules that properly release the GIL will run in parallel
Great option for I/O-bound applications

DISADVANTAGES:

cPython - subject to the GIL
Not interruptible/killable
If not following a command queue/message pump model (using the Queue module), then manual use of synchronization primitives become a necessity (decisions are needed for the granularity of locking)
Code is usually harder to understand and to get right - the potential for race conditions increases dramatically
'''

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")
