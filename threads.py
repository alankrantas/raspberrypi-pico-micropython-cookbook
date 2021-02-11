# Processing data on RPi Pico RP2040's dual cores


from _thread import start_new_thread, allocate_lock
import random, time


data = [x for x in range(20)]  # data to be processed

thread_started = False
thread_counter = 0

thread_lock = allocate_lock()  # lock resources for core 1

# thread task to be used by both cores
def task(task_id, is_thread):
    global thread_started, thread_counter
    
    if not thread_started:
        if is_thread:
            thread_started = True  # get core 1 ready
            time.sleep(1)
        else:
            while not thread_started:  # core 0 waits for core 1 ready
                pass
    
    while True:
        '''
        You can also use this if you only need to do things in core 1,
        which automatically calls acquire()/release():
        
        with is_thread:
            # process data in core 1
        '''
        
        if is_thread:
            thread_lock.acquire()
            
        if data:
            thread_counter += 1
            d = data.pop()
        else:
            break
        
        print('Thread {} processing: {} (counting: {})'.format(
            task_id, d, thread_counter))
        # simulate data processing time
        time.sleep(round(random.uniform(0.1, 0.5), 2))
        
        if is_thread:
            thread_lock.release()
    
    print('Thread {} ends'.format(task_id))
    if is_thread:
        thread_lock.release()


start_new_thread(task,(1, True))  # run task on core 1
task(0, False)                    # run task on core 0

time.sleep(1)
