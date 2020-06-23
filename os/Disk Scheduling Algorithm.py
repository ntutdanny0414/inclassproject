#0-4999
import random
import copy

def countmove(out):
    count = 0
    for i in range(len(out)-1):
        count = count + abs(out[i+1]-out[i])
    return count
def FCFS(start,requests):
    return [start]+requests
def SSTF(start,requests):
    out = []
    out.append(start)
    datalist = copy.copy(requests)
    move = copy.copy(start)
    while len(datalist) != 0:
        minnum = min(datalist, key=lambda x:abs(x-move))
        out.append(minnum)
        datalist.remove(minnum)
        move = minnum
    return out
def SCAN(start,requests):
    smallstart = []
    bigstart = []
    if start <= 2500:
        for i in range(len(requests)):
            if requests[i] <= start:
                smallstart.append(requests[i])
            else:
                bigstart.append(requests[i])
        smallstart = sorted(smallstart,reverse=True)
        bigstart = sorted(bigstart)
        return [start] + smallstart + [0] + bigstart
    else:
        for i in range(len(requests)):
            if requests[i] < start:
                smallstart.append(requests[i])
            else:
                bigstart.append(requests[i])
        smallstart = sorted(smallstart,reverse=True)
        bigstart = sorted(bigstart)
        return [start] + bigstart + [4999] + smallstart
def C_SCAN(start,requests):
    smallstart = []
    bigstart = []
    for i in range(len(requests)):
        if requests[i] < start:
            smallstart.append(requests[i])
        else:
            bigstart.append(requests[i])
    smallstart = sorted(smallstart)
    bigstart = sorted(bigstart)
    return [start] + bigstart + [4999] + [0] + smallstart
def LOOK(start,requests):
    smallstart = []
    bigstart = []
    if start <= 2500:
        for i in range(len(requests)):
            if requests[i] <= start:
                smallstart.append(requests[i])
            else:
                bigstart.append(requests[i])
        smallstart = sorted(smallstart,reverse=True)
        bigstart = sorted(bigstart)
        return [start] + smallstart + bigstart
    else:
        for i in range(len(requests)):
            if requests[i] < start:
                smallstart.append(requests[i])
            else:
                bigstart.append(requests[i])
        smallstart = sorted(smallstart,reverse=True)
        bigstart = sorted(bigstart)
        return [start] + bigstart  + smallstart
def C_LOOK(start,requests):
    smallstart = []
    bigstart = []
    for i in range(len(requests)):
        if requests[i] < start:
            smallstart.append(requests[i])
        else:
            bigstart.append(requests[i])
    smallstart = sorted(smallstart)
    bigstart = sorted(bigstart)
    return [start] + bigstart + smallstart

def main():
    requests = random.sample(range(5000), 1000)
    start = int(input('input start 0-4999:'))
    fcfs = FCFS(start,requests)
    sstf = SSTF(start,requests)
    scan = SCAN(start,requests)
    cscan = C_SCAN(start,requests)
    look = LOOK(start,requests)
    clook = C_LOOK(start,requests)
    print("  **********     FCFS       *********")
    print(countmove(fcfs))
    print("  **********     SSTF       *********")
    print(countmove(sstf))
    print("  **********     SCAN       *********")
    print(countmove(scan))
    print("  **********     C-SCAN     *********")
    print(countmove(cscan))
    print("  **********     LOOK       *********")
    print(countmove(look))
    print("  **********     C-LOOK     *********")
    print(countmove(clook))

main()
