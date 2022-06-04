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

led = Pin(25, Pin.OUT)
blink = lambda _: led.toggle()
    
Timer().init(mode=Timer.PERIODIC, period=500, callback=blink)
```

or

```python
from machine import Pin
import uasyncio

async def blink(led):
    while True:
        led.toggle()
        await uasyncio.sleep_ms(500)

uasyncio.run(blink(Pin(25, Pin.OUT)))
```

or

```python
from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    set(pins, 1)
    set(x, 31)                  [6]
    label('delay_high')
    nop()                       [29]
    jmp(x_dec, 'delay_high')

    set(pins, 0)
    set(x, 31)                  [6]
    label('delay_low')
    nop()                       [29]
    jmp(x_dec, 'delay_low')
    
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))
sm.active(1)
```

## Overclocking

The Pico has default frequency of 125 MHz but can be overclocked as high as **270 MHz** (which uses higher CPU voltage and might be less stable):

```python
from machine import freq

freq(270000000)
```

Remember to reset the frequency back to 125000000. (Note: firmware v1.18 seems fixed this problem.)

## NeoPIxel (WS2812) PIO Driver

The [NeoPixel driver](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/neopixel) is based on the official PIO example, repackaged into a class similar to CircuitPython's NeoPixel driver.

## DHT11/DHT22 PIO Driver

The [DHT driver](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/dht) is based on [Harry Fairhead & Mike James' DHT22 PIO code](https://www.i-programmer.info/programming/hardware/14572-the-pico-in-micropython-a-pio-driver-for-the-dht22.html?start=2), repackaged into a class similar to MicroPython's dht module on ESP boards.

## Multicore and Game of Life

[threads.py](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/blob/main/threads.py) is a simple example of how to run two tasks simultaneously on both of RP2040's cores.

There's also two versions of [Conway's Game of Life](https://github.com/alankrantas/raspberrypi-pico-micropython-cookbook/tree/main/game-of-life) with OLED display, with or without utilizing dual cores.

## Links

* [Raspberry Pi Pico - Getting Start with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/#getting-started-with-micropython)
* [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf)
* [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf)
* [Raspberry Pi Pico Python SDK Examples](https://github.com/raspberrypi/pico-micropython-examples)
