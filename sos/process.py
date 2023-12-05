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


def co2_x(vel_, temp, hy):
    x_co2 = np.arange(0, 0.05, 0.001)
    vels = np.array([vel(temp, hy, x) for x in x_co2])
    k, b = np.polyfit(vels, x_co2, 1)
    return k * vel_ + b


def read_array(path):
    return np.array(list(map(float, open(path, 'r').readlines()))) 


v1 = read_array('1mikro.txt')
v2 = read_array('2mikro.txt')
v1_ = read_array('gryaz1mikro.txt')
v2_ = read_array('gryaz2mikro.txt')
f = 500000


def t(v):
    return np.arange(0, len(v)) / f


def d(values):
    return np.array([0] + [values[i] - values[i - 1] for i in range(1, len(values))])


def front_index(vs):
    return peak(vs)


def peak(vs):
    imax = 0
    max = vs[imax]
    imin = 0
    min = vs[imin]
    for i, v in enumerate(vs):
        if v < min:
            imin = i
            min = vs[imin]
        if v > max:
            imax = i
            max = vs[imax]
        if max - v > 0.5 * (max - min):
            break
    return imax


def mean(v):
    return v.mean()
    

f2, a2 = plt.subplots()
a2.grid(color='lightgray')
a2.plot(t(v1), v1 - mean(v1), label='микрофон 2')
a2.plot(t(v2), v2 - mean(v2), label='микрофон 1')
# a2.plot(t(v1), d(v1), label='микрофон 2')
# a2.plot(t(v2), d(v2), label='микрофон 1')
a2.set_title('Звуковая волна в чистом воздухе')
a2.set_xlabel('Время t, с')
a2.set_ylabel('Звуковой сингал')
a2.legend()
f2.savefig('air.png')

vel1 = l * f / (np.argmax(v1[:1800]) - np.argmax(v2[:100]))
co2_x1 = co2_x(vel1, temp, hy)
print('скорость звука в чистом воздухе:', vel1)
print('концентрация УГ:', co2_x1)

f3, a3 = plt.subplots()
a3.grid(color='lightgray')
a3.plot(t(v1_), v1_ - mean(v1_), label='микрофон 2')
a3.plot(t(v2_), v2_ - mean(v2_), label='микрофон 1')
# a3.plot(t(v1_), d(v1_), label='микрофон 2')
# a3.plot(t(v2_), d(v2_), label='микрофон 1')
a3.set_title('Звуковая волна в грязном воздухе')
a3.set_xlabel('Время t, с')
a3.set_ylabel('Звуковой сингал')
a3.legend()
f3.savefig('co2.png')

vel2 = l * f / (np.argmax(v1_) - np.argmax(v2_))
co2_x2 = co2_x(vel2, temp, 1)
print('скорость звука в грязном воздухе:', vel2)
print('концентрация УГ:', co2_x(vel2, temp, 1))


x_co2 = np.arange(0, 0.1, 0.001)
vels = np.array([vel(temp, hy, x) for x in x_co2])
vels_gr = np.array([vel(temp, 1, x) for x in x_co2])
f1, a1 = plt.subplots()
a1.grid(color='lightgray')
a1.plot(x_co2, vels, label='чистый воздух')
a1.plot(x_co2, vels_gr, label='грязный воздух')
a1.scatter([co2_x1], [vel1], s=20)
a1.scatter([co2_x2], [vel2], s=20)
a1.set_title('Зависимость скорости звука от доли углекислого газа в воздухе')
a1.set_xlabel('Доля углекислого газа')
a1.set_ylabel('Скорость звука, м/с')
a1.legend()
f1.savefig('v_x.png')

plt.show()
