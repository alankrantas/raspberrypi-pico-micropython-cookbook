# Raspberrypi Pico MicroPython Cookbook

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

This is based on [the official PIO example](https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/neopixel_ring/neopixel_ring.py), repackaged into a class similar to CircuitPython's NeoPixel driver.

* [neopixel.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/neopixel/neopixel.py): the driver (contains test code so you can run this directly as well)
* [neopixel_test.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/neopixel/neopixel_test.py): test code (this is how you use it after uploaded the driver)

In the Thonny IDE open neopixel.py and go to File -> Save copy... -> Raspberry Pi Pico (note: the device has to be connected first). Save the driver as neopixel.py in Pico.

## Links

* [Raspberry Pi Pico - Getting Start with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/#getting-started-with-micropython)
* [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf)
* [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf)
* [Raspberry Pi Pico Python SDK Examples](https://github.com/raspberrypi/pico-micropython-examples)
