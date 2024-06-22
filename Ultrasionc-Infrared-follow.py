from machine import UART, Pin
from TRSensor import TRSensor
from Motor import PicoGo
from ws2812 import NeoPixel
from ST7789 import ST7789
import ujson
import utime


bat = machine.ADC(Pin(26))
temp = machine.ADC(4)

lcd = ST7789()
lcd.fill(0xF232)
lcd.line(2,2,70,2,0xBB56)
lcd.line(70,2,85,17,0xBB56)
lcd.line(85,17,222,17,0xBB56)
lcd.line(222,17,237,32,0xBB56)
lcd.line(2,2,2,118,0xBB56)
lcd.line(2,118,16,132,0xBB56)
lcd.line(17,132,237,132,0xBB56)
lcd.line(237,32,237,132,0xBB56)

lcd.text("Raspberry Pi Pico",90,7,0xFF00)
lcd.text("PicoGo",10,7,0x001F)
lcd.text("Waveshare.com",70,120,0x07E0)
lcd.show()

IR = Pin(5, Pin.IN)
M = PicoGo()
uart = UART(0, 9600)     # init with given baudrate
led = Pin(25, Pin.OUT)
led.value(1)
BUZ = Pin(4, Pin.OUT)
BUZ.value(0)

Buzzer = Pin(4, Pin.OUT)
DSR = Pin(2, Pin.IN)
DSL = Pin(3, Pin.IN)
Echo = Pin(15, Pin.IN)
Trig = Pin(14, Pin.OUT)
Trig.value(0)
Echo.value(0)

strip = NeoPixel()
strip.pixels_set(0, strip.BLACK)
strip.pixels_set(1, strip.BLACK)
strip.pixels_set(2, strip.BLACK)
strip.pixels_set(3, strip.BLACK)
strip.pixels_show()

LOW_SPEED    =  30
MEDIUM_SPEED =  50
HIGH_SPEED   =  80

speed = 20
t = 0
j = 0
n = 0  
def dist():
    Trig.value(1)
    utime.sleep_ms(10)
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
#     print("Distance:%6.2f cm" % dist())
#     utime.sleep(1)
    DR_status = DSR.value()
    DL_status = DSL.value()
    
    if((utime.ticks_ms() - t) > 3000):
        t=utime.ticks_ms()
        reading = temp.read_u16() * 3.3 / (65535)
        temperature = 27 - (reading - 0.706)/0.001721
        v = bat.read_u16()*3.3/65535 * 2
        p = (v - 3) * 100 / 1.2
        if(p < 0):p=0
        if(p > 100):p=100

        lcd.fill_rect(145,50,50,40,0xF232)
        lcd.text("temperature :  {:5.2f} C".format(temperature),30,50,0xFFFF)
        lcd.text("Voltage     :  {:5.2f} V".format(v),30,65,0xFFFF)
        lcd.text("percent     :   {:3.1f} %".format(p),30,80,0xFFFF)
        lcd.show()
    print(D)
    if(D<5):
        M.stop()
    elif((DL_status == 0) and (DR_status == 1)):
        M.left(20)
    elif((DL_status == 1) and (DR_status == 0)):
        M.right(20)
    elif(((D>5) and( D<7)) or ((DL_status == 0) and (DR_status == 0))):
        M.forward(30)
    else:
       M.stop() 
        
    utime.sleep_ms(20)
    

    for i in range(strip.num):
        strip.pixels_set(i, strip.wheel(((i * 256 // strip.num) + j) & 255))
    strip.pixels_show()
    j += 1
    if(j > 256): 
        j = 0







