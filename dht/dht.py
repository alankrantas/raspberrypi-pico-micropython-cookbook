from micropython import const
from machine import Pin
import rp2, time

class DHT:
    """
    DHT sensor driver class.
    The data pin has to be pulled up.
    Recommended querying interval: 1 sec (DHT11) or 2 secs (DHT22).
    
    Initialize:
        dht = dht.DHT(pin, model, [statemachine])
        
    Parameters
    --------------------
    pin : int
        GPIO number
    
    model : int
        DHT model (DHT.DHT_11 or DHT.DHT_22)
    
    statemachine : int
        State machine id (0~7)
    """
    
    __slot__ = ['_pin', '_model', '_humid', '_temp', '_cks', '_sm']
    
    DHT_11 = const(0)
    DHT_22 = const(1)
    
    @staticmethod
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW,
                 in_shiftdir=rp2.PIO.SHIFT_LEFT,
                 autopush=True)
    def _dht():
        """
        based on https://www.i-programmer.info/programming/hardware/14572-the-pico-in-micropython-a-pio-driver-for-the-dht22.html?start=1
        """
        
        set(pindirs, 1)
        set(pins, 1)
        pull(block)
        set(pins, 0)
        mov(x, osr)
        label('loop1')
        jmp(x_dec, 'loop1')
        set(pindirs, 0)
        wait(1, pin, 0)
        wait(0, pin, 0)
        wait(1, pin, 0)
        wait(0, pin, 0)
        set(y, 31)
        label('bits')
        wait(1, pin, 0)     [25]
        in_(pins, 1)
        wait(0, pin, 0)
        jmp(y_dec, 'bits')

        set(y, 7)
        label('check')
        wait(1, pin, 0)     [25]
        set(pins, 2)
        set(pins, 0)
        in_(pins, 1)
        wait(0, pin, 0)
        jmp(y_dec, 'check')
        push(block)
    
    def __init__(self, pin, model, statemachine=0):
        self._pin = Pin(pin)
        self._model = model if model in (DHT.DHT_11, DHT.DHT_22) else DHT.DHT_11
        self._humid = 0
        self._temp = 0
        self._cks = False
        self._sm = rp2.StateMachine(statemachine, DHT._dht, freq=490196,
                                    in_base=self._pin, set_base=self._pin, jmp_pin=self._pin)
        self._sm.active(1)
        
    def measure(self):
        """
        Query data from DHT sensor and calculate humidity/temperature readings.
        """

        self._sm.put(9000)
        data = self._sm.get()
        checksum = self._sm.get() & 0xFF
        
        byte_arr = [data >> 24 & 0xFF, data >> 16 & 0xFF, data >> 8 & 0xFF, data & 0xFF]
        self._cks = (checksum == sum(byte_arr) & 0xFF)
        
        if self._model == DHT.DHT_22:
            neg = -1 if (byte_arr[2] & 0x80) else 1
            byte_arr[2] &= 0x7F
            self._humid = (byte_arr[0] << 8 | byte_arr[1]) / 10
            self._temp = (byte_arr[2] << 8 | byte_arr[3]) / 10 * neg
        else:
            self._humid = byte_arr[0] + (byte_arr[1] / 100)
            self._temp = byte_arr[2] + (byte_arr[3] / 100)
    
    def humidity(self):
        """
        Return last humidity reading (%).
        
        Return value : float
        """
        
        return self._humid
    
    def temperature(self):
        """
        Return last temperature reading (Celsius).
        
        Return value : float
        """
        
        return self._temp
    
    def successful(self):
        """
        Return if the last checksum passed (query successful).
        
        Return value : bool
        """
        
        return self._cks


class DHT11(DHT):
    """
    DHT11 sensor driver class.
    The data pin has to be pulled up. Recommended querying interval: 1 sec.
    
    Initialize:
        dht = dht.DHT11(pin)
    
    Parameters
    --------------------
    pin : int
        GPIO number
    
    statemachine : int
        State machine id (0~7)
    """
    
    def __init__(self, pin, statemachine=0):
        super().__init__(pin, DHT.DHT_11, statemachine)


class DHT22(DHT):
    """
    DHT22 sensor driver class.
    The data pin has to be pulled up. Recommended querying interval: 2 secs.
    
    Initialize:
        dht = dht.DHT22(pin)
    
    Parameters
    --------------------
    pin : int
        GPIO number
    
    statemachine : int
        State machine id (0~7)
    """
    
    def __init__(self, pin, statemachine=0):
        super().__init__(pin, DHT.DHT_22, statemachine)


if __name__ == '__main__':
    
    import time
    
    dht = DHT11(28)
    
    while True:
    
        dht.measure()
        print('Humidity = {}%, temperature = {}C, checksum passed = {}'.format(
            dht.humidity(),
            dht.temperature(),
            dht.successful()
        ))
        time.sleep(2)
