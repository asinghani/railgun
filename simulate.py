import numpy as np
from math import log, sqrt

def ln(x):
    return log(abs(x))

def centi(x):
    return x / 100.0
def micro(x):
    return x / 1000000.0

u_over_4pi = 1e-7 # UNIVERSAL CONSTANT

# Projectile mass - kg
m = 0.01

# Rail separation
d = centi(1)

# Rail width
w = centi(0.3)

# Rail thickness
k = centi(2)

# Barrel length
L = 1.0

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
x = 0.01
v = 0

while x < L:
    t += DT
    x += v * DT

    integral_temperature_length = 20 * x # need to fix

    R_rail = (rho * x * (1 - 20*a) + rho * a * integral_temperature_length) / (w*k)
    R_total = 2 * R_rail + R_circuit

    I = Q / (R_total * C)
    Q -= I * DT

    left_lim = d - w/2.0
    right_lim = w/2.0
    F = 2 * u_over_4pi * I * I * (ln(left_lim) - ln(x * sqrt(left_lim**2 + x**2) + x**2) - ln(right_lim) + ln(x * sqrt(right_lim ** 2 + x ** 2) + x**2))

    a = F / m
    print(I)
    print(R_total)
    v += a * DT

print(x, v, t)
