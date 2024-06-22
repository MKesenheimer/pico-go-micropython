from machine import Pin
from TRSensor import TRSensor
from Motor import PicoGo
from ws2812 import NeoPixel
import time


M = PicoGo()
Buzzer = Pin(4, Pin.OUT)
DSR = Pin(2, Pin.IN)
DSL = Pin(3, Pin.IN)

strip = NeoPixel()
strip.pixels_set(0, strip.RED)
strip.pixels_set(1, strip.GREEN)
strip.pixels_set(2, strip.BLUE)
strip.pixels_set(3, strip.YELLOW)
strip.pixels_show()  
time.sleep(2)

TRS=TRSensor()
for i in range(100):
    if(i<25 or i>= 75):
        M.setMotor(30,-30)
    else:
        M.setMotor(-30,30)
    TRS.calibrate()
print("\ncalibrate done\r\n")
print(TRS.calibratedMin)
print(TRS.calibratedMax)
print("\ncalibrate done\r\n")
maximum = 100
integral = 0
last_proportional = 0
j=0

while True:
    position,Sensors = TRS.readLine()
    DR_status = DSR.value()
    DL_status = DSL.value()
    
    if((Sensors[0] + Sensors[1] + Sensors[2]+ Sensors[3]+ Sensors[4]) > 4000):
        Buzzer.value(0)
        M.setMotor(0,0)
    elif((DL_status == 0) or (DR_status == 0)):
        Buzzer.value(1)
        M.setMotor(0,0)
    else:
        Buzzer.value(0)
        # The "proportional" term should be 0 when we are on the line.
        proportional = position - 2000

        # Compute the derivative (change) and integral (sum) of the position.
        derivative = proportional - last_proportional
        #integral += proportional

        # Remember the last position.
        last_proportional = proportional
        
        '''
        // Compute the difference between the two motor power settings,
        // m1 - m2.  If this is a positive number the robot will turn
        // to the right.  If it is a negative number, the robot will
        // turn to the left, and the magnitude of the number determines
        // the sharpness of the turn.  You can adjust the constants by which
        // the proportional, integral, and derivative terms are multiplied to
        // improve performance.
        '''
        power_difference = proportional/30  + derivative*2;  

        if (power_difference > maximum):
            power_difference = maximum
        if (power_difference < - maximum):
            power_difference = - maximum

        if (power_difference < 0):
            M.setMotor(maximum + power_difference, maximum)
        else:
            M.setMotor(maximum, maximum - power_difference)

    for i in range(strip.num):
        strip.pixels_set(i, strip.wheel(((i * 256 // strip.num) + j) & 255))
    strip.pixels_show()
    j += 1
    if(j > 256): 
        j = 0
