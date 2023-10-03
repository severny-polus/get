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
    return [int(b) for b in format(d, 'b').zfill(depth)]

def b2d(b):
    return sum([k * 2 ** (depth - 1 - i) for (i, k) in enumerate(b)])

depth = 8

def adc():
    value = [0] * depth
    for k in range(depth):
        value[k] = 1
        GPIO.output(dac, value)
        time.sleep(0.001)
        if GPIO.input(comp) == GPIO.HIGH:
            value[k] = 0
    d = b2d(value)
    return d

try:
    while True:
        a = adc()
        print('{}: {:.3f}V'.format(str(a).zfill(3), a / 2 ** depth * 3.3))
        time.sleep(0.1)
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

