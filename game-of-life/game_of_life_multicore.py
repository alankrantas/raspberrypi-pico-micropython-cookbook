import urandom, utime, gc
from _thread import allocate_lock, start_new_thread, exit
from machine import Pin, ADC, I2C, freq
from micropython import const
from ssd1306 import SSD1306_I2C  # https://github.com/stlehmann/micropython-ssd1306


freq(260000000)  # overclock to 260 MHz

gc.enable()
urandom.seed(sum([ADC(2).read_u16() for _ in range(100)]))


RULE     = ((3, ), (2, 3))  # birth/survival: B3/S23
WIDTH    = const(128)
HEIGHT   = const(64)
DOT_SIZE = const(3)
RAND_PCT = const(25)  # %
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


i2c = I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.fill(0)
display.show()

lock = allocate_lock()


print('Conway\'s Game of Life: matrix size {} x {}'.format(X, Y))


def calculate_cells(is_thread):
    while task:
        try:
            with lock:
                i = task.pop()
        except:
            break
        i1 = (i - 1) if (i % X) - 1 >= 0 else (i - 1) + X
        i3 = (i + 1) if (i % X) + 1 < X else (i + 1) - X
        cells = board[i1] + board[i3] + \
                board[i1 - X] + board[i - X] + board[i3 - X] + \
                board[(i1+X)%TOTAL] + board[(i+X)%TOTAL] + board[(i3+X)%TOTAL]
        if cells in RULE[board[i]]:
            buffer[i] = 1
    if is_thread:
        exit()


def draw_cells(is_thread):
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
        exit()


t = 0

while True:
    start = utime.ticks_ms()
    
    gen += 1
    print('Gen {}: {} cell(s) ({} ms)'.format(gen, sum(board), t))
    
    task = list(range(TOTAL))
    display.fill(0)
    start_new_thread(draw_cells, (True, ))
    draw_cells(False)
    while task:
        pass
    display.show()
    
    task = list(range(TOTAL))
    buffer = bytearray([0] * TOTAL)
    start_new_thread(calculate_cells, (True, ))
    calculate_cells(False)
    while task:
        pass
    board = buffer
    
    t = utime.ticks_diff(utime.ticks_ms(), start)
