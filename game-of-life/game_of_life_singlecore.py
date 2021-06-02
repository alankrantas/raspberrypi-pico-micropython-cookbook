import urandom, utime, gc
from machine import Pin, I2C, freq
from micropython import const
from ssd1306 import SSD1306_I2C  # https://github.com/stlehmann/micropython-ssd1306

gc.enable()
freq(270000000)  # overclock to 270 MHz


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
board  = [0 if urandom.randint(0, (100 // RAND_PCT) - 1) else 1 for _ in range(TOTAL)]
gen    = 0

i2c = I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.fill(0)
display.show()


print('Conway\'s Game of Life: matrix size {} x {}'.format(X, Y))
    

def calculate_next_gen():
    global board
    buffer = [0] * TOTAL
    for i in range(TOTAL):
        i1 = (i - 1) if (i % X) - 1 >= 0 else (i - 1) + X
        i3 = (i + 1) if (i % X) + 1 < X else (i + 1) - X
        cells = board[i1] + board[i3] + \
                board[i1 - X] + board[i - X] + board[i3 - X] + \
                board[(i1+X)%TOTAL] + board[(i+X)%TOTAL] + board[(i3+X)%TOTAL]
        if cells in RULE[board[i]]:
            buffer[i] = 1
    board = buffer


def display_board():
    display.fill(0)
    for i in range(TOTAL):
        if board[i]:
            display.fill_rect((i % X) * DOT_SIZE, (i // X) * DOT_SIZE, DOT_SIZE, DOT_SIZE, 1)
    display.show()


t1, t2 = 0, 0

while True:
    gen += 1
    print('Gen {}: {} cell(s) (board = {} ms, draw = {} ms)'.format(gen, sum(board), t2, t1))
    
    start = utime.ticks_ms()
    display_board()
    t1 = utime.ticks_diff(utime.ticks_ms(), start)
    
    start = utime.ticks_ms()
    calculate_next_gen()
    t2 = utime.ticks_diff(utime.ticks_ms(), start)
