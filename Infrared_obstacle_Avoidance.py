import utime
from Motor import PicoGo
from machine import Pin

M = PicoGo()
DSR = Pin(2, Pin.IN)
DSL = Pin(3, Pin.IN)

while True:
    DR_status = DSR.value()
    DL_status = DSL.value()

    if((DL_status == 0) and (DR_status == 0)):
        M.left(10)
    elif((DL_status == 0) and (DR_status == 1)):
        M.right(10)
    elif((DL_status == 1) and (DR_status == 0)):
        M.left(10)
    else:
        M.forward(20)
        
    utime.sleep_ms(10)
