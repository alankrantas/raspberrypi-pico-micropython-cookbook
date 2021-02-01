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

## Links

* [Raspberry Pi Pico - Getting Start with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/#getting-started-with-micropython)
* [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf)
* [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf)
* [Raspberry Pi Pico Python SDK Examples](https://github.com/raspberrypi/pico-micropython-examples)
