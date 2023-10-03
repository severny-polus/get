import RPi.GPIO as GPIO
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

def d2b(d):
    return [int(b) for b in format(d, 'b').zfill(depth)]

def b2d(b):
    return sum([k * 2 ** (depth - 1 - i) for (i, k) in enumerate(b)])

depth = 8

def adc_simple_():
    i = 0
    GPIO.output(dac, d2b(i))
    while GPIO.input(comp) == GPIO.LOW and i < 2 ** depth - 1:
        i += 1
        GPIO.output(dac, d2b(i))
    return i

def adc_simple():
    n = 3
    for i in range(n):
        a = adc_simple_()
        if a > 0:
            return a
        time.sleep(0.01)
    return 0

def adc_sar_():
    value = [0] * depth
    for k in range(depth):
        value[k] = 1
        GPIO.output(dac, value)
        if GPIO.input(comp) == GPIO.HIGH:
            value[k] = 0
        time.sleep(0.001)
    d = b2d(value)
    return d

def adc_sar():
    n = 2
    aa = [0] * n
    for i in range(n):
        aa[i] = adc_sar_()
        time.sleep(0.01)
    return sum(aa) // n

try:
    while True:
        a = adc_simple()
        time.sleep(0.1)
        
        level = a // 32
        volume = [i <= level for i in range(8)]
        GPIO.output(leds, volume)
        
        print('{}: {:.3f}V'.format(str(a).zfill(3), a / 2 ** depth * 3.3))
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()


