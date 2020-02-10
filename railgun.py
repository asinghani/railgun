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

    # Projectile mass - kg
    m = getty_mass + 0.001 * p * (rail_separation - rail_width) * projectile_thickness * rail_thickness

    # Step size of simulation - seconds
    DT = 0.000002

    ##### Persistant State
    Q = C * V
    t = 0
    x = 0.5
    v = 0.0

    energy = 0.0

    temperature_array = np.array([20.0] * int(L * 1000))

    proj_temp = 20.0
    proj_width = rail_separation - rail_width

    iters = 0

    I_initial = None

    current_arr = []

    while x < L:
        iters = iters + 1
        t += DT
        x += v * DT

        # Calculate Resistance
        integral_temperature_length = temperature_array.sum() / 1000.0

        R_rail = (rho * x * (1.0 - 20.0*a) + rho * a * integral_temperature_length) / (w*k)
        R_projectile = (rho * proj_width * (1.0 - 20.0*a) + rho * a * proj_temp * proj_width) / (rail_thickness * projectile_thickness)
        R_total = 2 * R_rail + R_projectile + R_circuit

        # Capacitor Current
        if use_capacitor:
            I = Q / (R_total * C)
            Q -= I * DT

            energy += I * I * R_total * DT
        else:
            I = fixed_voltage / R_total

            energy += fixed_voltage * I * DT


        if I_initial is None:
            I_initial = I

        # Force on Projectile
        left_lim = d - w/2.0
        right_lim = w/2.0
        F = 2 * u_over_4pi * I * I * (ln(left_lim) - ln(x * sqrt(left_lim**2 + x**2) + x**2) - ln(right_lim) + ln(x * sqrt(right_lim ** 2 + x ** 2) + x**2))

        accel = F / m - 9.81
        v += accel * DT

        deltaT = I * I * R_rail * DT / (p * x * w * k * c)
        temperature_array[0:min(int(x * 1000), len(temperature_array))] += deltaT

        proj_temp += I * I * R_projectile * DT / (p * proj_width * projectile_thickness * rail_thickness * c)

        current_arr.append(v)

        #print(round(x, 2), round(v, 2), round(a, 2), round(F, 2), round(I, 2))

    return (x, v, t, temperature_array, proj_temp, R_total, I_initial, I, iters, energy, current_arr)

