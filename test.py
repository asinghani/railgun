import numpy as np
from railgun import run_sim

# needed velocity = 11200 m/s

getty_mass = 90

getty_depth = 0.95
getty_width = 0.3
projectile_thickness = 0.1

rail_width = 0.2
barrel_length = 4.0

resistance = 0.0001
voltage = 13000.0

out = run_sim(getty_mass = getty_mass,
        rail_separation = getty_depth + rail_width,
        rail_width = rail_width,
        rail_thickness = getty_width,
        projectile_thickness = projectile_thickness,
        barrel_length = barrel_length,
        power_circuit_resistance = resistance,
        use_capacitor = False,
        capacitor_voltage = 0.0,
        total_capacitance = 0.0,
        fixed_voltage = voltage)

(x, v, t, temperature_array, proj_temp, R_total, I_initial, I_final, iters, energy, current_arr) = out

print(round(x, 2), round(v, 2), t, round(temperature_array.max(), 2), round(proj_temp, 2), round(R_total, 5), I_initial, iters, energy)

#print(current_arr[::4])

from matplotlib import pyplot as plt
import numpy as np

with plt.xkcd():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    #plt.yticks([])

    #plt.annotate('T', xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

    plt.plot(current_arr)

    plt.xlabel("Time")
    plt.ylabel("Velocity (m/s)")

plt.tight_layout()
plt.show()
