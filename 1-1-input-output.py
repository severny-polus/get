import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN)
a = GPIO.input(20)
GPIO.output(21, a)
time.sleep(1)

GPIO.cleanup()
