import threading
import time
data = [90 ,81 ,78 ,95 ,79 ,72 ,85]
out = []
def findave(data):
    out.append(int(sum(data) / len(data)))
    time.sleep(1)
def findmin(data):
    min_n = data[0]
    for i in range(1,len(data)):
        if data[i] < min_n:
            min_n = data[i]
    
    out.append(min_n)
    time.sleep(1)
def findmax(data):
    max_n = data[0]
    for i in range(1,len(data)):
        if data[i] > max_n:
            max_n = data[i]
    
    out.append(max_n)
    time.sleep(1)
threads = []
threads.append(threading.Thread(target = findave, args = (data,)))
threads.append(threading.Thread(target = findmin, args = (data,)))
threads.append(threading.Thread(target = findmax, args = (data,)))

threads[0].start()
threads[1].start()
threads[2].start()

threads[0].join()
threads[1].join()
threads[2].join()
print('The average value is '+str(out[0]))
print('The minimum value is '+str(out[1]))
print('The maximum value is '+str(out[2]))
