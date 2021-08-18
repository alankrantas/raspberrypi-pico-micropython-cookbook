## DHT11/DHT22 Sensor PIO Driver

This driver is based on [Harry Fairhead & Mike James' DHT22 PIO code](https://www.i-programmer.info/programming/hardware/14572-the-pico-in-micropython-a-pio-driver-for-the-dht22.html?start=2), repackaged into a class similar to MicroPython's dht module on ESP boards.

The driver contains some test code as well (will not run as part of the driver). You can run it directly from your computer.

In the Thonny IDE open **dht.py** and go to **File** -> **Save copy...** -> **Raspberry Pi Pico** (the device has to be connected first). Save the driver as **dht.py** in Pico.

## Wiring Example

![Untitled Sketch_bb](https://user-images.githubusercontent.com/44191076/129920511-e2e7ba2d-118a-428d-9d83-16fe1435604f.png)

* VCC -> 3.3V or 5V
* DATA/OUT -> GPIO 28 (Pin 34), has to be pulled up
* NC -> (not connected)
* GND -> GND

The 3-pin DHT11 and DHT22 models don't have NC pin and usually has built-in resistor to pull up the DATA pin.

It is recommended to wait 1 sec (DHT11) or 2 secs (DHT22) between two queries.

## Test Code

```python
import time
from machine import Pin
from dht import DHT11, DHT22
    
dht = DHT11(Pin(28))
# for DHT22, use dht = DHT22(Pin(28))
    
while True:
    
    dht.measure()
    print('Humidity = {}%, temperature = {}C, checksum passed = {}'.format(
        dht.humidity(),
        dht.temperature(),
        dht.successful()
    ))
    time.sleep(2)
```
