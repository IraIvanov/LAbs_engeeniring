import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def deciaml_to_binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def num_to_dac(value):
    signal = deciaml_to_binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    value = 7
    num = 0
    for i in range(8):
        num += 2**value
        signal = num_to_dac(num)
        voltage = num / 256 * 3.3
        time.sleep(0.007)
        comp_value = GPIO.input(comp)
        if comp_value == 0:
            num -= 2**value
        value -= 1
    print("ADC value= {:^3} -> {}, voltage = {:.2f}".format(num, signal, voltage))



try:
    while True:
        adc()
finally:
    GPIO.output(dac , 0)


