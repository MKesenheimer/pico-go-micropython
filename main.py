# https://www.waveshare.com/wiki/PicoGo

from TRSensor import TRSensor
from Motor import PicoGo
import time
from ST7789 import ST7789

lcd = ST7789()
lcd.build_frame()
lcd.text("Line-Tracking", 10, 30, 0xFFFF)
lcd.show()

time.sleep(1)
m = PicoGo()
trs = TRSensor()
#for i in range(100):
#    p = 30
#    if(i<25 or i>=75):
#        m.setMotor(p, -p)
#    else:
#        m.setMotor(-p, p)
#    trs.calibrate()

# TEST
trs.fixed_calibration()

lcd.build_frame()
lcd.text("Calibration done", 10, 40, 0xFFFF)
lcd.show()

integral = 0
last_proportional = 0

## good sets
# maximum = 20
#p = 0.015
#i = 0.0003
#d = 0.01

#maximum = 25
#p = 0.02
#i = 0.0003
#d = 0.02

maximum = 25
p = 0.02
i = 0.0004
d = 0.02

while True:
    position, sensors = trs.readLine()
    sensorsum = sum(sensors)
    #sensorsum = 7000
    if(sensorsum > 6000):
        lcd.build_frame()
        lcd.text(str(sensors), 10, 30, 0xFFFF)
        lcd.text(str(trs.calibratedMin), 10, 40, 0xFFFF)
        lcd.text(str(trs.calibratedMax), 10, 50, 0xFFFF)
        lcd.text(f"position = {position - 3000}", 10, 60, 0xFFFF)
        lcd.show()
        m.setMotor(0, 0)
    else:
        # The "proportional" term should be 0 when we are on the line.
        proportional = position - 3000

        # Compute the derivative (change) and integral (sum) of the position.
        derivative = proportional - last_proportional
        integral += proportional
        if integral >= 1000:
            integral = 1000
        elif integral <= -1000:
            integral = -1000

        # Remember the last position.
        last_proportional = proportional
        power_difference = proportional * p  + derivative * d + integral * i
        
        lcd.build_frame()
        lcd.text(f"position     = {position}", 10, 30, 0xFFFF)
        lcd.text(f"proportional = {proportional * p}", 10, 40, 0xFFFF)
        lcd.text(f"derivative   = {derivative * d}", 10, 50, 0xFFFF)
        lcd.text(f"integral     = {integral * i}", 10, 60, 0xFFFF)
        lcd.text(f"power_difference = {power_difference}", 10, 70, 0xFFFF)
        lcd.show()
        
        if (power_difference > maximum):
            power_difference = maximum
        if (power_difference < - maximum):
            power_difference = - maximum
        
        if (power_difference > 0):
            m.setMotor(maximum - power_difference, maximum)
        else:
            m.setMotor(maximum, maximum + power_difference)