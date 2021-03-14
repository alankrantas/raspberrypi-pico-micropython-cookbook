# Raspberrypi Pico MicroPython Cookbook

Updating...

## Blinky

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

while True:
    led.toggle()
    time.sleep(0.5)

```

or

```python
from machine import Pin, Timer

Timer().init(mode=Timer.PERIODIC, period=500,
             callback=lambda _: Pin(25, Pin.OUT).toggle())
```

## SSD1306 OLED

Use this driver here (which is the same as the one in ESP ports):

https://github.com/stlehmann/micropython-ssd1306

```python
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(27), sda=Pin(26), freq=400000)  # sofeware I2C
display = SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.text('Raspberry Pi', 0, 8, 1)
display.text('Pico!', 0, 16, 1)
display.show()

```

Or:

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)  # hardware I2C
display = SSD1306_I2C(128, 64, i2c)
```

## NeoPIxel (WS2812) driver

This is based on [the official PIO example](https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio/neopixel_ring), repackaged into a class similar to CircuitPython's NeoPixel driver.

* [neopixel.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/neopixel/neopixel.py): the driver (contains test code so you can run this directly as well)
* [neopixel_test.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/neopixel/neopixel_test.py): test code (this is how you use it after uploaded the driver)

In the Thonny IDE open neopixel.py and go to File -> Save copy... -> Raspberry Pi Pico (note: the device has to be connected first). Save the driver as neopixel.py in Pico.

## Threads on dual cores

[threads.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/threads.py) is a simple example of how to run two tasks simultaneously on both of RP2040's cores.

There's also two versions of [Conway's Game of Life](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/game-of-life) with OLED display, with or without utilizing dual cores.

## Links

* [Raspberry Pi Pico - Getting Start with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/#getting-started-with-micropython)
* [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf)
* [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf)
* [Raspberry Pi Pico Python SDK Examples](https://github.com/raspberrypi/pico-micropython-examples)
