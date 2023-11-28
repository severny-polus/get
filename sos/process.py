import numpy as np
import matplotlib.pyplot as plt

temp = 21.2
hy = 0.345
l = 1.16
R = 8.31
mu_air = 28.97
mu_water = 18.01
mu_co2 = 44.01
Cp_air = 1.0036
Cp_water = 1.863
Cp_co2 = 0.838
Cv_air = 0.7166
Cv_water = 1.403
Cv_co2 = 0.649
mus = np.array([mu_air, mu_water, mu_co2]) / 1000
Cps = np.array([Cp_air, Cp_water, Cp_co2])
Cvs = np.array([Cv_air, Cv_water, Cv_co2])

def vel(temp, hy, x_co2):
    T = temp + 273.15
    x_water = 2642.4 * hy / 10**5
    xs = np.array([1 - x_water - x_co2, x_water, x_co2])
    mu = np.dot(mus, xs)
    Cp = np.dot(Cps * mus, xs)
    Cv = np.dot(Cvs * mus, xs)
    gamma = Cp / Cv
    return (gamma * R * T / mu) ** 0.5


x_co2 = np.arange(0, 0.05, 0.001)
vels = np.array([vel(temp, hy, x) for x in x_co2])
vels_gr = np.array([vel(temp, 1, x) for x in x_co2])
f1, a1 = plt.subplots()
a1.grid(color='lightgray')
a1.plot(x_co2, vels, label='чистый воздух')
a1.plot(x_co2, vels_gr, label='грязный воздух')
a1.set_title('Зависимость скорости звука от доли углекислого газа в воздухе')
a1.set_xlabel('Доля углекислого газа')
a1.set_ylabel('Скорость звука, м/с')
a1.legend()
f1.savefig('v_x.png')

def co2_x(vel_, temp, hy):
    x_co2 = np.arange(0, 0.05, 0.001)
    vels = np.array([vel(temp, hy, x) for x in x_co2])
    k, b = np.polyfit(vels, x_co2, 1)
    return k * vel_ + b

v1 = np.array(list(map(float, open('1mikro.txt', 'r').readlines())))
v2 = np.array(list(map(float, open('2mikro.txt').readlines())))
v1_ = np.array(list(map(float, open('gryaz1mikro.txt').readlines())))
v2_ = np.array(list(map(float, open('gryaz2mikro.txt').readlines())))
f = 500000

def t(v):
    return np.arange(0, len(v)) / f
    
f2, a2 = plt.subplots()
a2.grid(color='lightgray')
a2.plot(t(v1), v1 - v1.mean(), label='микрофон 2')
a2.plot(t(v2), v2 - v2.mean(), label='микрофон 1')
a2.set_title('Звуковая волна в чистом воздухе')
a2.set_xlabel('Время t, с')
a2.set_ylabel('Звуковой сингал')
a2.legend()
f2.savefig('air.png')

vel1 = l * f / (np.argmax(v1[:1800]) - np.argmax(v2[:100]))
print('скорость звука в чистом воздухе:', vel1)
print('концентрация УГ:', co2_x(vel1, temp, hy))

f3, a3 = plt.subplots()
a3.grid(color='lightgray')
a3.plot(t(v1_), v1_ - v1_.mean(), label='микрофон 2')
a3.plot(t(v2_), v2_ - v2_.mean(), label='микрофон 1')
a3.set_title('Звуковая волна в грязном воздухе')
a3.set_xlabel('Время t, с')
a3.set_ylabel('Звуковой сингал')
a3.legend()
f3.savefig('co2.png')

vel2 = l * f / (np.argmax(v1_) - np.argmax(v2_))
print('скорость звука в грязном воздухе:', vel2)
print('концентрация УГ:', co2_x(vel2, temp, 1))

plt.show()
