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

def run_sim(getty_mass, rail_separation, rail_width, rail_thickness, projectile_thickness, barrel_length, power_circuit_resistance, use_capacitor, capacitor_voltage = 0.0, total_capacitance = 0.0, fixed_voltage = 0.0):
    # Projectile mass - kg
    m = getty_mass + 0.001 * p * (rail_separation - rail_width) * projectile_thickness * rail_thickness

    # Rail separation
    d = rail_separation

    # Rail width
    w = rail_width

    # Rail thickness
    k = rail_thickness

    # Barrel length
    L = barrel_length

    # Resistivity at 20C (metal)
    rho = 1.59e-8

    # Resistivity expansion coefficient (metal)
    a = 0.0038

    # Power circuit resistance
    R_circuit = power_circuit_resistance

    # Capacitor charge voltage
    V = capacitor_voltage

    # Total capacitance
    C = total_capacitance

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

    proj_temp = 20.0
    proj_width = rail_separation - rail_width

    while x < L:
        t += DT
        x += v * DT

        # Calculate Resistance
        integral_temperature_length = temperature_array.sum() / 1000.0

        R_rail = (rho * x * (1 - 20*a) + rho * a * integral_temperature_length) / (w*k)
        R_projectile = (rho * proj_width * (1 - 20*a) + rho * a * proj_temp * proj_width) / (rail_thickness * projectile_thickness)
        R_total = 2 * R_rail + R_projectile + R_circuit

        # Capacitor Current
        if use_capacitor:
            I = Q / (R_total * C)
            Q -= I * DT
        else:
            I = fixed_voltage / R_total

        # Force on Projectile
        left_lim = d - w/2.0
        right_lim = w/2.0
        F = 2 * u_over_4pi * I * I * (ln(left_lim) - ln(x * sqrt(left_lim**2 + x**2) + x**2) - ln(right_lim) + ln(x * sqrt(right_lim ** 2 + x ** 2) + x**2))

        a = F / m
        v += a * DT

        deltaT = I * I * R_rail * DT / (p * x * w * k * c)
        proj_temp += I * I * R_rail * DT / (p * x * w * k * c)

        temperature_array[0:min(int(x * 1000), len(temperature_array))] += deltaT

        # TODO Calculate heat flow


    print("Final Position", x)
    print("Final Velocity", v)
    print("Time to exit barrel", t)
    print("Maximum temperature", temperature_array.max())

    return (x, v, t, temperature_array.max())

