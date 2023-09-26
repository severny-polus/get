import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def d2b(n):
    return [int(b) for b in format(n, 'b').zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]
number = d2b(85)
GPIO.setup(dac, GPIO.OUT, initial=0)
GPIO.output(dac, number)
time.sleep(15)

GPIO.output(dac, 0)
GPIO.cleanup()