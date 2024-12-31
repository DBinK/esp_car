from machine import Pin, SPI
from random import randint
from lib.st7789 import ST7789

@micropython.viper
def rect(buff:ptr16, x:int, y:int, w:int, h:int, c:int):
    b, L = ptr16(buff), int(w*h)
    sx = int(x+(y*240))
    for i in range(L):
        b[sx+(240*(i//w))+i%w] = c

display = ST7789(
    spi     = SPI(2, sck=Pin(40, Pin.OUT), mosi=Pin(41, Pin.OUT)),
    dc      = Pin(38, Pin.OUT),
    rst     = Pin(42, Pin.OUT),
    cs      = Pin(39, Pin.OUT),
    baud    = 62_500_000,
    bright  = 0xFF,
    rot     = 0,
    buff    = memoryview(bytearray(115200))
)

class Thing:
    def __init__(self, x:int, y:int, w:int, h:int, c:int, sx:int, sy:int):
        self.x, self.y   = x, y
        self.w, self.h   = w, h
        self.sx, self.sy = sx, sy
        self.c = c
        self.xr = range(240-w+1)
        self.yr = range(240-h+1)
        
    def update(self):
        self.sx = self.sx if self.sx+self.x in self.xr else -self.sx
        self.sy = self.sy if self.sy+self.y in self.yr else -self.sy
        self.x += self.sx
        self.y += self.sy
        rect(display.buffer, self.x, self.y, self.w, self.h, self.c)
 
        
def make_things(cnt:int = 5):
    things = [0]*cnt
    for n in range(cnt):
        a = randint(20, 40)
        things[n] = Thing(randint(0, 240-a), randint(0, 240-a), a, a, randint(0xF000, 0xFFFF), randint(4, 8), randint(4, 8))
    return things      
        
things = make_things(50)

while True:
    display.clear_buff(randint(0x0000, 0x7F7F))
    
    for t in things:
        t.update()
    
    display.update_buff()