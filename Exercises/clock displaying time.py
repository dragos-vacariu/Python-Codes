import time

#Function time.ctime() will display the current time in
#               DayName-Month-DayDate-Hour-Minute-Second-Year format

#Function time.time() will only display the time stamp.
def Clock():
    while True:
        print("Time: " + str(time.ctime()))
        time.sleep(1) # wait 1 second before displaying this again.

Clock()
