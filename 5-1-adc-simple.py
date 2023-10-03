import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)

def d2b(d):
    return [int(b) for b in format(d, 'b').zfill(8)]

depth = 8

def adc():
    i = 0
    GPIO.output(dac, d2b(i))
    while GPIO.input(comp) == GPIO.LOW and i < 2 ** depth - 1:
        i += 1
        GPIO.output(dac, d2b(i))
    return i

def adc_fix():
    n = 3
    for i in range(n):
        a = adc()
        if a > 0:
            return a
        time.sleep(0.01)
    return 0

try:
    while True:
        a = adc_fix()
        print('{}: {:.3f}V'.format(str(a).zfill(3), a / 2 ** depth * 3.3))
        time.sleep(0.1)
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
