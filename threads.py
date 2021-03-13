# Processing data on RPi Pico RP2040's dual cores


from _thread import start_new_thread, allocate_lock
import _thread, random, time


data = [random.randint(1, 100) for x in range(10)]  # data to be processed


thread_finished = False
lock = allocate_lock()


def task(is_thread):   
    global thread_finished
    
    while True:

        try:
            with lock:
                d = data.pop()
            '''
            You can also use
                lock.acquire()
            and
                lock.release()
            around the shared resources.
            '''
        except:
            if not data:
                break
            
        print('Thread (id: {}) processing: {}'.format(
            _thread.get_ident(), d))
        
        # simulate data processing time
        time.sleep(round(random.uniform(0.1, 0.3), 2))
    
    print('Thread (id: {}) ends'.format(_thread.get_ident()))
    if is_thread:
        # signal that task on core 1 is finished
        with lock:
            thread_finished = True
        _thread.exit()


start_new_thread(task, (True, ))  # run task on core 1
task(False)                       # run task on core 0

while not thread_finished:  # wait for task on core 1
    pass
