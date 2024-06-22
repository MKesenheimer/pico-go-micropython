import utime
from machine import Pin
from Motor import PicoGo

M = PicoGo()
Echo = Pin(15, Pin.IN)
Trig = Pin(14, Pin.OUT)
Trig.value(0)
Echo.value(0)

def dist():
    Trig.value(1)
    utime.sleep_us(10)
    Trig.value(0)
    while(Echo.value() == 0):
        pass
    ts=utime.ticks_us()
    while(Echo.value() == 1):
        pass
    te=utime.ticks_us()
    distance=((te-ts)*0.034)/2
    return distance

while True:
    D = dist()
    if(D <= 20):
        M.right(20)
        #Ab.left()
    else:
        M.forward(20)
        
    utime.sleep_ms(20)
