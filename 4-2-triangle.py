import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=0)

def d2b(n):
    return [int(b) for b in format(n, 'b').zfill(8)]

m = 255
try:
    T = float(input())
    while True:
        for i in range(2 * m):
            v = i if i <= m else 2 * m - i
            b = d2b(v)
            GPIO.output(dac, b)
            print("{:.3f}".format(v / (m + 1) * 3.3) + 'V')
            time.sleep(T / (2 * m))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
