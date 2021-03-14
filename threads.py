# Processing data on RPi Pico RP2040's dual cores

import _thread, random, time


# data to be processed
task = [random.randint(1, 100) for x in range(10)]

# lock for shared resources
lock = _thread.allocate_lock()

task_done = False


def worker(worker_id, is_thread):
    global task_done

    while task:

        try:
            with lock:
                d = task.pop()  # retrieve available task
            '''
            You can also use
                lock.acquire()
            and
                lock.release()
            around the shared resources.
            '''
        except:
            break
        
        # process data
        print('Thread {} processing: {}'.format(worker_id, d))
        
        # simulate data processing time
        time.sleep(round(random.uniform(0.1, 0.5), 2))
    
    print('Thread {} ends'.format(worker_id))
    if is_thread:
        task_done = True
        _thread.exit()  # exit thread on core 1


_thread.start_new_thread(worker, (1, True))  # process task on core 1
worker(0, False)                             # process task on core 0

while not task_done:  # wait for core 1 finished tasks
    pass
