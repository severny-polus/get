import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
number = [0, 0, 0, 1, 1, 0, 0, 0]
GPIO.setup(dac, GPIO.OUTPUT)
GPIO.output(dac, number)
time.sleep(10)

GPIO.cleanup()