import spidev
import time

########################################
#   Open, use and close SPI ADC
########################################

########################################
# Do not forget to setup GPIO pins to SPI functions!
#
# Enter the followig commands into RPi terminal:
#
# raspi-gpio get
# raspi-gpio set 9 a0
# raspi-gpio set 10 a0
# raspi-gpio set 11 a0
# raspi-gpio get
########################################

# 160 -> 1680
# 140 -> 1480
# 120 -> 1280
# 100 -> 1080
# 80 -> 900
# 60 -> 700
# 40 -> 510

clock_blue = 23
cs_yellow = 8
input_green = 9

spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC have been initialized")

def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    initSpiAdc()
    data = []
    start = time.time()
    while time.time() - start < 60:
        adc = getAdc()
        data.append(adc)
        
    with open('roman-fiz.txt', 'w') as f:
        for v in data:
            f.write(str(v) + '\n')
finally:
    deinitSpiAdc()
