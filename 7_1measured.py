import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
measures = []
time_start = time.time()


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

#Вспомогательные функции
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
        #signal = deciaml_to_binary(num)
        voltage = num / 256 * 3.3
        time.sleep(0.007)
        comp_value = GPIO.input(comp)
        if comp_value == 0:
            num -= 2**value
        value -= 1
    print("ADC value= {:^3} -> {}, voltage = {:.2f}".format(num, signal, voltage))
    return num


try:
    measure = 0
    GPIO.output(troyka, 1)
    #Зарядка 
    while measure/3.13 < 0.97:
        time_first = time.time()
        volume = adc()/255*8
        GPIO.output(leds , 0)
        measure = volume*255/8/ 256 * 3.3
        print(measure/3.13)
        measures.append(measure)
        for i in range(int(volume)):
            GPIO.output(leds[7-i], 1)
        time_second = time.time()
        time_x = time_second - time_first
    GPIO.output(troyka, 0)
    #Разрядка
    while measure/3.3 > 0.1:
        volume = adc()/255*8
        GPIO.output(leds , 0)
        measure = volume*255/8/ 256 * 3.3
        print(measure)
        measures.append(measure)
        for i in range(int(volume)):
            GPIO.output(leds[7-i], 1)
    time_end = time.time()
    time_measures = time_end - time_start
    friq = 1 / time_x
    print("Время измерений:", time_measures)
    print("Частота:",friq)
    print("Время одного измерения:", time_x)
    print("Шаг квантования:", 3.3/256)
    plt.plot(measures)
    plt.show()
    forwrite = [friq, 3.3/256]
    forwrite_str = [str(item) for item in forwrite ]
    #print(measures)
    measures_str = [str(item) for item in measures ]  
    #Запись в файл
    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(measures_str))
    with open("settings.txt", "w") as outfile:
        outfile.write("\n".join(forwrite_str))
finally:
    GPIO.output(dac , 0)