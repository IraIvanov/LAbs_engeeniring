import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

m_data = []

leds = [21, 20, 16, 12, 7, 8, 25, 24]
count = 0

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
GPIO.setmode(GPIO.BCM)
for elem in leds:
    GPIO.setup(elem, GPIO.OUT)

for i in range(8):
    GPIO.output(leds[i], 1)
    time.sleep(0.2)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def getnum(arr):
    num = 0
    for i in range(8):
        num += arr[i] * (2 ** (7 - i))
    return num

def adc():
    arr = [0, 0, 0, 0, 0, 0, 0, 0]
    num = 0
    for i in range (8):
        
        arr[i] = 1
        num = getnum(arr)

        if i == 8:
            return 
        
        num2dac(num)
        time.sleep(0.01)

        compval = GPIO.input(comp)
        
        if (compval == 0):
            arr[i] = 0
    ans = num / 256 * 3.3

    
    
    return num
    


GPIO.setmode(GPIO.BCM)
for elem in dac:
    GPIO.setup(elem, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)
start = time.time()
GPIO.output(troyka, 1)

try:
    while True:
        GPIO.output(troyka, 1)
        napr = adc()
        time.sleep(1)
        GPIO.output(leds, decimal2binary(napr))
        m_data.append(napr / 256 * 3.3)
    
        if ((napr / 256 * 3.3) > 2):
            break
        
        
    GPIO.output(troyka, 0)
    while True:
      
        napr = adc()
        time.sleep(1)
        GPIO.output(leds, decimal2binary(napr))
        m_data.append(napr / 256 * 3.3)
        if ((napr / 256 * 3.3) < 0.5):
            break
    stop = time.time()
    print("Time ", stop - start)
    plt.plot(m_data)
    
    m_data = [str(item) for item in m_data]
    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(m_data))
    plt.show()
        
        
finally:
    for elem in leds:
        GPIO.output(elem, 0)
    GPIO.output(troyka, 0)

    GPIO.cleanup()