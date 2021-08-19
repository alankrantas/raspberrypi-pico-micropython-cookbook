## NeoPixel (WS2812) PIO Driver

This driver is based on [the official PIO example](https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio/neopixel_ring), repackaged into a class similar to CircuitPython's NeoPixel driver.

The driver contains some test code as well (will not run as part of the driver). You can run it directly from your computer.

To use the driver, in the Thonny IDE open **neopixel.py** and go to **File** -> **Save copy...** -> **Raspberry Pi Pico** (the device has to be connected first). Save the driver as **neopixel.py** in Pico.

## Wiring Examlple

![pico_neopixel](https://user-images.githubusercontent.com/44191076/111096225-fc939700-8579-11eb-886a-1db53321a151.png)

* VIN -> 3.3V or 5V (5V is brighter)
* GND -> GND
* DIN/DI -> GPIO 28 (Pin 34)

(A push button is added between RUN (pin 30) and GND as the reset button. It's not needed for the NeoPixel driver.)

DIN can be any of the pins. If you want to connect more than one NeoPixel strips to the same pin, connect DOUT/DO to the next strip's DIN/DI, and connect VIN/GND as well. 

Each WS2812 LED comsumes about 50 mA at max level. The 3.3V pin on Pico can saftly output at least 300 mA.

## Test Code

```python
from neopixel import NeoPixel # Upload the driver first!
import time

# a strip of 12 LEDs at GPIO 28, brightness level 30%, do not auto write after any changes
neo = NeoPixel(28, n=12, brightness=0.3, autowrite=False)
    
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
    neo.fill(color)  # fill the whole strip with a specific color
    neo.show()  # write changes into LEDs (automatically executed if autowrite=True)
    time.sleep(0.25)

# chase
for color in COLORS:       
    for i in range(neo.n):
        neo[i] = color  # set a LED with a specific color
        neo.show()
        time.sleep(0.025)

# rainbow
for i in range(255):
    neo.rainbow_cycle(i)  # set all LEDs to rainbow color (position 0-255)
    neo.show()
    time.sleep(0.0025)
    
# rotate
for _ in range(neo.n * 3):
    neo.rotate(clockwise=True)  # rotate exsisting LED colors clockwise or counter-clockwise
    neo.show()
    time.sleep(0.05)
        
neo.clear()  # clear all colors (set to black)
neo.show()
```
