from machine import Pin, ADC, I2C
from micropython import const
from ssd1306 import SSD1306_I2C
import urandom, utime, gc, _thread

gc.enable()
urandom.seed(sum([ADC(2).read_u16() for _ in range(1000)]))


BIRTH    = (3, )
SURVIVAL = (2, 3)
WIDTH    = const(128)
HEIGHT   = const(64)
DOT_SIZE = const(3)
RAND_PCT = const(25)
SCL_PIN  = const(27)
SDA_PIN  = const(26)


X      = WIDTH // DOT_SIZE
Y      = HEIGHT // DOT_SIZE
TOTAL  = X * Y
board  = bytearray([0 if urandom.randint(0, (100 // RAND_PCT) - 1) else 1
                    for _ in range(TOTAL)])
buffer = bytearray([])
task   = []
gen    = 0


display = SSD1306_I2C(WIDTH, HEIGHT,
                      I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000))
display.fill(0)
display.show()

thread_done = False
lock = _thread.allocate_lock()


print('Conway\'s Game of Life: matrix size {} x {}'.format(X, Y))


def calculate_cells(is_thread):
    global thread_done
    while task:
        try:
            with lock:
                i = task.pop()
        except:
            break
        group = board[i-1:i+2] + \
                board[(i-1-X)%TOTAL:(i+2-X)%TOTAL] + \
                board[(i-1+X)%TOTAL:(i+2+X)%TOTAL]
        cells = sum(group)
        if not board[i]:
            if cells in BIRTH:
                with lock:
                    buffer[i] = 1
        else:
            if (cells - 1) in SURVIVAL:
                with lock:
                    buffer[i] = 1
    if is_thread:
        with lock:
            thread_done = True
        _thread.exit()


def draw_cells(is_thread):
    global thread_done
    while task:
        try:
            with lock:
                i = task.pop()
        except:
            break
        if board[i]:
            display.fill_rect((i % X) * DOT_SIZE,
                              (i // X) * DOT_SIZE,
                              DOT_SIZE, DOT_SIZE, 1)
    if is_thread:
        with lock:
            thread_done = True
        _thread.exit()

gen, start, t = 0, 0, 0

while True:
    gc.collect()
    gen += 1
    print('Gen {}: {} cell(s) ({} ms)'.format(gen, sum(board), t))
    
    task = list(range(TOTAL))
    thread_done = False
    
    display.fill(0)
    _thread.start_new_thread(draw_cells, (True, ))
    draw_cells(False)
    while not thread_done:
        pass
    display.show()
    
    buffer = bytearray([0] * TOTAL)
    task = list(range(TOTAL))
    thread_done = False
    
    start = utime.ticks_ms()
    
    _thread.start_new_thread(calculate_cells, (True, ))
    calculate_cells(False)
    while not thread_done:
        pass
    board = buffer
    
    t = utime.ticks_diff(utime.ticks_ms(), start)
