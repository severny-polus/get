import RPi.GPIO as GPIO
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]
GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

for i in range(3):
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(led, GPIO.LOW)
        
GPIO.output(leds, GPIO.LOW)
GPIO.cleanup(leds)
