import threading
import schedule
import time

def print_words(words):
    print(words)
    # print("I'm running on thread %s" % threading.current_thread())

def run_threaded(job_func, words):
    # print(words)
    job_thread = threading.Thread(target = job_func, args = words)
    job_thread.start()
    return schedule.CancelJob


def run_threaded_not_cancel(job_func, words):
    # print(words)
    job_thread = threading.Thread(target = job_func, args = words)
    job_thread.start()

schedule.every(1).seconds.do(run_threaded, print_words, "一")
schedule.every(1).seconds.do(run_threaded_not_cancel, print_words, "二")
schedule.every(1).seconds.do(run_threaded_not_cancel, print_words, "三")
schedule.every(1).seconds.do(run_threaded, print_words, "四")

while True:
    for i in range(5):
        schedule.run_pending()
        time.sleep(3)
    break
print(schedule.jobs)
schedule.clear()
print("clear jobs!")
print(schedule.jobs)