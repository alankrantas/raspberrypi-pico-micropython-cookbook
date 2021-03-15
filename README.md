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

## NeoPIxel (WS2812) driver

The [NeoPixel driver](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/neopixel) is based on the official PIO example, repackaged into a class similar to CircuitPython's NeoPixel driver.

## Multicore and Game of Life

[threads.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/threads.py) is a simple example of how to run two tasks simultaneously on both of RP2040's cores.

There's also two versions of [Conway's Game of Life](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/game-of-life) with OLED display, with or without utilizing dual cores.

## Links

* [Raspberry Pi Pico - Getting Start with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/#getting-started-with-micropython)
* [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf)
* [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf)
* [Raspberry Pi Pico Python SDK Examples](https://github.com/raspberrypi/pico-micropython-examples)
