import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pwm_pin = 21
GPIO.setup(pwm_pin, GPIO.OUT, initial=0)


pwm = GPIO.PWM(pwm_pin, 1000)
pwm.start(0)

try:
    while True:
        dc = float(input())
        pwm.ChangeDutyCycle(dc)
        print("{:.3f}".format(dc / 100 * 3.3) + 'V')
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.output(pwm_pin, 0)
    GPIO.cleanup()
