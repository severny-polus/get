import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

F = 0
dU = 0
with open('settings.txt', 'r') as f:
    F = float(f.readline().split('=')[-1])
    dU = float(f.readline().split('=')[-1])
    
U = np.genfromtxt('data.txt')
t = np.arange(0, len(U)/F, 1/F)
tmax = t[U.argmax()]
Umin = U[-10]
tmin = t[np.where(U == Umin)][0]

fig, ax = plt.subplots(figsize=(12, 9))
ax.grid(which='major', color='lightgray')
ax.grid(which='minor', ls=':', color='lightgray')
ax.plot(t, U, color='blue', label='U(t)', marker='.', ms=10, markevery=int(round(F))//2)
ax.set_xlabel('Время, с')
ax.set_ylabel('Напряжение, В')
ax.set_title('Процесс заряда и разряда конденсатора в RC-цепочке')
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

ax.text(2, 0.4, 'Время зарядки: {:.2f}c'.format(tmax))
ax.text(9, 0.4, 'Время разрядки: {:.2f}c'.format(tmin - tmax))

ax.legend()
fig.savefig('plot.svg')
plt.show()
