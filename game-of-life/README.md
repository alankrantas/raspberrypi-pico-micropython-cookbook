## Conway's Game of Life on Raspberry Pi Pico - using SSD1306 OLED

Here are two versions of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), either use or not use dual cores of the RP2040 processor (which can be overclocked to 270 MHz). For the game calculation itself, the speed of the multicore version is about 60-70% of the single core version.

## Parameters

```python
# Cellular automaton rule: https://en.wikipedia.org/wiki/Life-like_cellular_automaton
# Here is Conway's rule B3/S23
RULE     = ((3, ), (2, 3))  # (birth, survival)

# Size of the OLED
WIDTH    = const(128)
HEIGHT   = const(64)

# dot size to be drawn (the bigger the size, the smaller the game board)
DOT_SIZE = const(3)  # 3x3 pixels (so the board size is 42 x 21)
RAND_PCT = const(25)  # 25% chance cell generation in the initial board

# SCL/SDA pins of the OLED
SCL_PIN  = const(27)
SDA_PIN  = const(26)
```

### SSD1306 OLED Driver

Use this driver here (which is the same as the one in MicroPython's ESP ports):

https://github.com/stlehmann/micropython-ssd1306

Since MicroPython v1.14, you have to choose either hardware or software I2C bus for Pico and ESP32:

```python
from machine import Pin, SoftI2C, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)  # hardware I2C(1)
# i2c = SoftI2C(scl=Pin(27), sda=Pin(26), freq=400000)  # sofeware I2C

display = SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.text('Raspberry Pi', 0, 8, 1)
display.text('Pico!', 0, 16, 1)
display.show()

```

Software I2C bus can be any of the pins. Check out the [pinout](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/rpi-pico-pinout.jpg) to see where are hardware I2C pins (I2C(0) and I2C(1)).

### Wiring

A 0.96" 128x64 pixels OLED display is used here:

![pico_oled](https://user-images.githubusercontent.com/44191076/111094673-be48a880-8576-11eb-935b-a82cb6eca983.png)

* VCC -> 3.3V or 5V
* GND -> GND
* SCL -> GPIO 27 (Pin 32)
* SDA -> GPIO 26 (Pin 31)

A push button is added between RUN (pin 30) and GND as the reset button. The code also use ADC(2) (GPIO 28/Pin 34)'s floating values as the random seed.
