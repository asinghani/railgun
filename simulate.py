import numpy as np
from math import log, sqrt
import matplotlib.pyplot as plt

def ln(x):
    return log(abs(x))

def centi(x):
    return x / 100.0
def micro(x):
    return x / 1000000.0

u_over_4pi = 1e-7 # UNIVERSAL CONSTANT

def run_sim(z):
    # Projectile mass - kg
    m = 0.01

    # Rail separation
    d = centi(z)

    # Rail width
    w = d / 5.0 #centi(0.3)

    # Rail thickness
    k = centi(2)

    # Barrel length
    L = 0.1

    # Resistivity at 20C (metal)
    rho = 1.59e-8

    # Resistivity expansion coefficient (metal)
    a = 0.0038

    # Power circuit resistance
    R_circuit = 0.03

    # Capacitor charge voltage
    V = 400.0

    # Total capacitance
    C = 16 * micro(3300)

    # Density (metal, gram per cubic meter)
    p = 10500000

    # Specific heat (metal, per gram)
    c = 0.240

    # Step size of simulation - seconds
    DT = 0.001

    ##### Persistant State
    Q = C * V
    t = 0
    x = 0.001
    v = 0.0

    temperature_array = np.array([20.0] * int(L * 1000))

    while x < L:
        t += DT
        x += v * DT

        integral_temperature_length = temperature_array.sum() / 1000.0

        R_rail = (rho * x * (1 - 20*a) + rho * a * integral_temperature_length) / (w*k)
        R_total = 2 * R_rail + R_circuit

        I = Q / (R_total * C)
        Q -= I * DT

        left_lim = d - w/2.0
        right_lim = w/2.0
        F = 2 * u_over_4pi * I * I * (ln(left_lim) - ln(x * sqrt(left_lim**2 + x**2) + x**2) - ln(right_lim) + ln(x * sqrt(right_lim ** 2 + x ** 2) + x**2))

        a = F / m

        deltaT = I * I * R_rail * DT / (p * x * w * k * c)
        temperature_array[0:min(int(x * 1000), len(temperature_array))] += deltaT

        v += a * DT

    print("Final Position", x)
    print("Final Velocity", v)
    print("Time to exit barrel", t)
    print("Maximum temperature", temperature_array.max())

    return (x, v, t, temperature_array.max())

values_x = []
values_y = []
values_y2 = []

for i in np.linspace(0.05, 2.5, num=50).tolist():
    x, v, t, temp = run_sim(i)
    values_x.append(i)
    values_y.append(v)
    values_y2.append(temp)


fig, ax1 = plt.subplots()
ax1.set_xlabel("Rail Separation (cm) : Rail width = 1/5 rail separation")

ax1.plot(values_x, values_y, color="r")
ax1.set_ylabel("Velocity", color='r')

ax2 = ax1.twinx()
ax2.plot(values_x, values_y2, color="b")
ax2.set_ylabel("Temperature", color='b')
plt.show()

#plt.imshow(temperature_array.reshape((1, len(temperature_array))), aspect = "auto", cmap="viridis", interpolation = "bicubic")
#plt.show()
