from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print("Run task %s (%s)..." % (name, os.getpid()))
    while True:
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print("Task %s run %0.f seconds." % (name, (end - start)))

if __name__ == "__main__":
    print("Parent process %s." % os.getpid())
    p = Pool(4)
    p.apply_async(long_time_task, args=(1,))
    p.apply_async(long_time_task, args=(2,))

    print("Waiting for all subprocess done...")
    p.close()
    p.join()
    print("All subprocess done.")