import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

with open('settings.txt', 'r') as settings:
    tmp = [ float(i) for i in settings.read().split("\n")]
    #print(tmp)

data_array = np.loadtxt("data.txt", dtype = float)

#print(data_array)
time = len(data_array)/tmp[0]
time_up = data_array.argmax()/tmp[0]
time_low = time - time_up
time_array = np.arange(0, time ,1/tmp[0])
print(time)
print(time_up)
print(time_low)
fig, ax = plt.subplots(figsize = (16,10), dpi = 400)
ax.plot(time_array, data_array, '-b', label='V(t)', markevery = 25, marker = "s")
ax.set_ylabel('Напряжение, В')
ax.set_xlabel('Время, с')
ax.text(16, .10, r'Время зарядки = 27.2 с Время разрядки = 22.7')
#ax.annoate('Время зарядки = 27.2 с Время разрядки = 22.7 с', xy=(2, 1), xytext=(3, 1.5))
ax.set_title('Процесс заряда и разряда конденсатора в RC - цепочке')
ax.legend();
#ax.scatter(time_array , data_array)
ax.minorticks_on()


plt.xlim(0, 50)
plt.ylim(0, 3.5)
ax.yaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
plt.grid(which = 'minor')
plt.grid()
fig.savefig("fig.svg")
#plt.show()