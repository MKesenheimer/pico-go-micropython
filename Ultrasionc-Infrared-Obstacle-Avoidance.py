import utime
from machine import Pin
from Motor import PicoGo

M = PicoGo()
DSR = Pin(2, Pin.IN)
DSL = Pin(3, Pin.IN)
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
    DR_status = DSR.value()
    DL_status = DSL.value()
    if((D <= 20) or (DL_status == 0) or (DR_status == 0)):
        M.right(20)
        #Ab.left()
    else:
        M.forward(40)
        
    utime.sleep_ms(20)
