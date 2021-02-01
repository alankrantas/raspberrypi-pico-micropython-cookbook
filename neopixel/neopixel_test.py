# NeoPixel (WS2812) test for Raspberry Pi Pico/MicroPython
# Upload the driver first!


from neopixel import NeoPixel
import time


neo = NeoPixel(28, n=8, brightness=0.3, autowrite=False)
    
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, BLACK)


# fill
for color in COLORS:       
    neo.fill(color)
    neo.show()
    time.sleep(0.25)

# chase
for color in COLORS:       
    for i in range(neo.n):
        neo[i] = color
        neo.show()
        time.sleep(0.025)

# rainbow
for i in range(255):
    neo.rainbow_cycle(i)
    neo.show()
    time.sleep(0.0025)
    
# rotate
for _ in range(neo.n * 3):
    neo.rotate(clockwise=True)
    neo.show()
    time.sleep(0.05)
        
neo.clear()
neo.show()
