# NeoPixel (WS2812) driver for Raspberry Pi Pico/MicroPython
# 
# based on the official PIO example:
# https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/neopixel_ring/neopixel_ring.py
#
# How to upload this driver in Thonny IDE:
# File -> Save copy... -> Raspberry Pi Pico -> Save this file as "neopixel.py"


from machine import Pin
import rp2, array


class NeoPixel:
    """
    NeoPixel (WS2812) driver class.
    
    Initialize:
        neo = neopixel.NeoPixel(pin, [n, brightness, autowrite])
        
    Parameters
    --------------------
    pin : int
        GPIO number
    
    n : int
        Number of leds (default 1)
    
    brightness : float
        Percentage of brightness level (0.0~1.0, default 1.0)
    
    autowrite : bool
        Automatically call .show() whenever buffer is changed (default False)
    """
    
    __slot__ = ['pin', 'n', 'brightness', 'autowrite', 'buffer', 'sm']
    
    def __init__(self, pin, n=1, brightness=1.0, autowrite=False):
        self.pin = Pin(pin, Pin.OUT)
        self.brightness = brightness
        self.autowrite = autowrite
        self.sm = rp2.StateMachine(0, NeoPixel._ws2812, freq=8_000_000, sideset_base=self.pin)
        self.sm.active(1)
        self.buffer = [(0, 0, 0)] * n
        if not self.autowrite:
            self.show()

    def __getitem__(self, key):
        return self.buffer[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self[key:key+1] = [value]
        elif isinstance(key, slice):
            self.buffer[key] = [tuple(color) for color in value]
            if self.autowrite:
                self.show()

    def __len__(self):
        return len(self.buffer)

    @property
    def n(self):
        return len(self.buffer)

    def fill(self, color):
        """
        Fill a specific color to all leds.
        
        Parameters
        --------------------
        color : list or tuple
            (r, g, b)
        """
        self[:] = [color] * self.n
        if self.autowrite:
            self.show()
    
    def clear(self):
        """
        Clear all leds.
        """
        self.fill((0, 0, 0))

    def rainbow_cycle(self, cycle=0):
        """
        Set rainbow colors accross all leds.
        
        Parameters
        --------------------
        cycle : int
            Cycle (0~255) of rainbow colors (default 0)
        """
        self[:] = [NeoPixel._wheel((round(i * 255 / self.n) + cycle) & 255) for i in range(self.n)]
        if self.autowrite:
            self.show()
            
    def rotate(self, clockwise=True):
        """
        Rotate current buffer clockwise or counter-clockwise.
        
        Parameters
        --------------------
        clockwise : bool
            Rotate counterwise (Default True; False = counter-clockwise)
        """
        self[:] = self[-1:] + self[:-1] if clockwise else self[1:] + self[:1]
        if self.autowrite:
            self.show()

    def show(self):
        """
        Write buffer to leds via state machine.
        """
        self.brightness = NeoPixel._between(self.brightness, 0.0, 1.0)
        uint16_arr = array.array('I', [0] * self.n)
        for i, color in enumerate(self.buffer):
            r, g, b = color[0], color[1], color[2]
            r = NeoPixel._between(round(r * self.brightness), 0, 255)
            g = NeoPixel._between(round(g * self.brightness), 0, 255)
            b = NeoPixel._between(round(b * self.brightness), 0, 255)
            uint16_arr[i] = (g << 16) | (r << 8) | b
        self.sm.put(uint16_arr, 8)
        
    # for programmable pin state machine
    @staticmethod
    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def _ws2812():
        T1 = 3
        T2 = 3
        T3 = 4
        wrap_target()
        label('bitloop')
        out(x, 1)               .side(0)    [T3 - 1]
        jmp(not_x, 'do_zero')   .side(1)    [T1 - 1]
        jmp('bitloop')          .side(1)    [T2 - 1]
        label('do_zero')
        nop()                   .side(0)    [T2 - 1]
        wrap()

    # for generating rainbow colors
    @staticmethod
    def _wheel(pos):
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    # for limiting a value between an interval
    @staticmethod
    def _between(value, minV, maxV):
        return max(min(value, maxV), minV)


# ------------------------------------------------------------
# Test sample:

if __name__ == '__main__':
    
    import time
    
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
        neo.fill(color)
        neo.show()
        time.sleep(0.25)

    # chase
    for color in COLORS:       
        for i in range(neo.n):
            neo[i] = color
            neo.show()
            time.sleep(0.025)

    # rainbow
    for i in range(255):
        neo.rainbow_cycle(i)
        neo.show()
        time.sleep(0.0025)
    
    # rotate
    for _ in range(neo.n * 3):
        neo.rotate(clockwise=True)
        neo.show()
        time.sleep(0.05)
        
    neo.clear()
    neo.show()
