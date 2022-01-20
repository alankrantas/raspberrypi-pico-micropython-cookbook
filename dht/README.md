## DHT11/DHT22 Sensor PIO Driver

This driver is based on [Harry Fairhead & Mike James' DHT22 PIO code](https://www.i-programmer.info/programming/hardware/14572-the-pico-in-micropython-a-pio-driver-for-the-dht22.html?start=2), repackaged into a class similar to MicroPython's dht module on ESP boards.

The driver contains some test code as well (will not run as part of the driver). You can run it directly from your computer.

To use the driver, in the Thonny IDE open **dht.py** and go to **File** -> **Save copy...** -> **Raspberry Pi Pico** (the device has to be connected first). Save the driver as **dht.py** in Pico.

## Wiring Example

![Untitled Sketch_bb](https://user-images.githubusercontent.com/44191076/129920511-e2e7ba2d-118a-428d-9d83-16fe1435604f.png)

* VCC -> 3.3V or 5V
* DATA/OUT -> GPIO 28 (Pin 34), has to be pulled up with a 10 KΩ resistor, unless you are using the 3-pin PCB module
* NC -> (not connected)
* GND -> GND

The 3-pin DHT11 and DHT22 modules don't have NC pin and usually has a built-in resistor to pull up the DATA pin.

You can change the data pin to any of the GPIOs.

## Test Code

```python
from dht import DHT, DHT11, DHT22
import time
    
dht = DHT11(28)
# for DHT22, use
#       dht = DHT22(28)
# or
#       dht11 = DHT(28, DHT.DHT_11)
#       dht22 = DHT(28, DHT.DHT_22)
    
while True:
    
    dht.measure()
    print('Humidity = {}%, temperature = {}C, checksum passed = {}'.format(
        dht.humidity(),
        dht.temperature(),
        dht.successful()  # if the checksum of last query indicates good data
    ))
    time.sleep(2)  # DHT11 should wait at least 1 sec between queries and DHT22 should wait 2 secs
```

It is recommended to wait at least 1 sec (DHT11) or 2 secs (DHT22) between two queries.

## Setting State Machine

If you are going to use this driver with other PIO drivers, you need to specify a state machine to avoid instruction conflict:

```python
dht = DHT11(28, statemachine=1)
```

Pico has 2 PIO blocks and each has 4 state machines (which runs the PIO instructions), make it total 8 (number 0~7, default 0).
