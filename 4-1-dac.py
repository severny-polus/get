import RPi.GPIO as GPIO


dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=0)

def d2b(n):
    return [int(b) for b in format(n, 'b').zfill(8)]
    
loop = True
while loop:
    s = input()
    if s == 'q':
        loop = False
        continue
    
    try:
        n = int(s)
    except ValueError:
        print('Не удалось распознать целое число')
        continue
    
    if n not in range(256):
        print('Число выходит за допустимые границы [0;255]')
        continue
    
    b = d2b(n)
    GPIO.output(dac, b)
    print("{:.3f}".format(n / 256 * 3.3) + 'V')

GPIO.output(dac, 0)
GPIO.cleanup()
