import threading
import time
import itertools

c = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
sem = threading.Semaphore()

# global variable for thread
times = 0

# global iterator for array
i = 0
#===============================================================
def pop():
    global i
    print(c[i:i+4])
    i = i+1

def push():
    global i
    c.insert(i+3, 'X')

# reader: keep reading 3 items from list
def reader():
    global times
    while True:
        sem.acquire()
        #===Reader===
        pop()
        pop()
        
        
        #===Reader===
        sem.release()
        time.sleep(0.25)
        
        if times >= 23:
            break
        

# insert X in list
def writer():
    global times
    while True:
        sem.acquire()
        #===Writer===
        push()
        #===Writer===
        sem.release()
        time.sleep(0.25)
        times = times + 1
        if times >= 23:
            break

t = threading.Thread(target = reader)
t.start()
t2 = threading.Thread(target = writer)
t2.start()
