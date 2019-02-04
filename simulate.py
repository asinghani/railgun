import numpy as np

def centi(x):
    return x / 100.0
def micro(x):
    return x / 1000000.0

u_over_4pi = 1e-7 # UNIVERSAL CONSTANT

# Rail separation
d = centi(2)

# Rail width
w = centi(1)

# Rail thickness
k = centi(2)

# Barrel length
L = 1.0

# Resistivity at 20C (metal)
rho = 1.59e-8

# Resistivity expansion coefficient (metal)
a = 0.0038

# Power circuit resistance
R_circuit = 0.001

# Capacitor charge voltage
V = 400

# Total capacitance
C = 16 * micro(3300)

# Density (metal, gram per cubic meter)
p = 10500000

# Specific heat (metal, per gram)
c = 0.240
