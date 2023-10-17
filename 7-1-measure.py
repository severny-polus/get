import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)

depth = 8

def d2b(d):
    return [int(b) for b in format(d, 'b').zfill(depth)]

def b2d(b):
    return sum([k * 2 ** (depth - 1 - i) for (i, k) in enumerate(b)])

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

def decimal2volts(d):
    return d * 3.3 / (2 ** depth - 1)

def adc_volts():
    return decimal2volts(adc())

vmax = 224

data = []

try:
    # Ход эксперимента
    t = time.time()
    GPIO.output(troyka, GPIO.HIGH)
    down = False
    while True:
        value = adc()
        if value >= vmax:
            GPIO.output(troyka, GPIO.LOW)
            down = True
        if down and value <= 0:
            break
        volts = decimal2volts(value)
        data.append(volts)
        print('{:.3f}V'.format(volts))
        
    # Определение и вывод параметров
    T = time.time() - t
    dt = T / len(data)
    f = 1 / dt
    dv = decimal2volts(1)
    print('длительность эксперимента:', T, 'с')
    print('период измерения:', dt, 'с')
    print('частота дискретизации:', f, 'Гц')
    print('шаг квантования:', dv, 'В')
    
    # Запись данных в файлы
    with open('data.txt', 'w') as f:
        for v in data:
            f.write(str(v) + '\n')
            
    with open('settings.txt', 'w') as f:
        f.write('f=' + str(f) + '\n')
        f.write('dv=' + str(dv) + '\n')
    
    # Построение графика
    plt.grid(color='lightgray', zorder=1)
    plt.plot(data, zorder=2)
    plt.xlabel('номер измерения')
    plt.ylabel('напряжение на конденсаторе, В')
    plt.savefig('plot.png')
    
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

