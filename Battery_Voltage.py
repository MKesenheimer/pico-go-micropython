from machine import Pin
from ST7789 import ST7789
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
lcd.line(2,118,17,132,0xBB56)
lcd.line(17,132,237,132,0xBB56)
lcd.line(237,32,237,132,0xBB56)

lcd.text("Raspberry Pi Pico",90,7,0xFF00)
lcd.text("PicoGo",10,7,0x001F)
lcd.text("Waveshare.com",70,120,0x07E0)
lcd.show()

while (1):
    utime.sleep(1)
    reading = temp.read_u16() * 3.3 / (65535)
    temperature = 27 - (reading - 0.706)/0.001721
    v = bat.read_u16()*3.3/65535 * 2
    p = (v - 3) * 100 / 1.2
    if(p < 0):p=0
    if(p > 100):p=100

    lcd.fill_rect(145,50,65,40,0xF232)
    lcd.text("temperature :  {:5.2f} C".format(temperature),30,50,0xFFFF)
    lcd.text("Voltage     :  {:5.2f} V".format(v),30,65,0xFFFF)
    lcd.text("percent     :   {:3.1f} %".format(p),30,80,0xFFFF)

    lcd.show()
