import urandom, utime, gc, _thread
from machine import Pin, ADC, I2C
from micropython import const
from ssd1306 import SSD1306_I2C  # https://github.com/stlehmann/micropython-ssd1306


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
board  = [0 if urandom.randint(0, (100 // RAND_PCT) - 1) else 1 for _ in range(TOTAL)]
buffer = [0 for _ in range(TOTAL)]
gen    = 0


display = SSD1306_I2C(WIDTH, HEIGHT,
                      I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000))
display.fill(0)
display.show()


print('Conway\'s Game of Life: matrix size {} x {}'.format(X, Y))
    

def calculate_next_gen():
    global board
    for i in range(TOTAL):
        group = board[i-1:i+2] + \
                board[(i-1-X)%TOTAL:(i+2-X)%TOTAL] + \
                board[(i-1+X)%TOTAL:(i+2+X)%TOTAL]
        cells = sum(group)
        if not board[i]:
            buffer[i] = 1 if (cells in BIRTH) else 0
        else:
            buffer[i] = 1 if ((cells - 1) in SURVIVAL) else 0
    board[:] = buffer


def display_board():
    for i in range(TOTAL):
        display.fill_rect((i % X) * DOT_SIZE,
                          (i // X) * DOT_SIZE,
                          DOT_SIZE, DOT_SIZE, board[i])
    display.show()


gen, start, t = 0, 0, 0

while True:
    gen += 1
    print('Gen {}: {} cell(s) ({} ms)'.format(gen, sum(board), t))
    display_board()

    start = utime.ticks_ms()
    calculate_next_gen()
    t = utime.ticks_diff(utime.ticks_ms(), start)
