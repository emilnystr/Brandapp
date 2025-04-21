import numpy as np
from numba.typed import List

#Materialdatabas i Numba-kompatibel form, blir en lista av tuples såhär: (material 1, material 2)
material_databas = List()
material_databas.append((  # Betong
    np.array([0, 20, 100, 101, 120, 121, 200, 250, 300, 350, 400, 500, 600, 1200], dtype=np.float32),
    np.array([2, 2, 1.75, 1.75, 1.7, 1.7, 1.55, 1.5, 1.35, 1.3, 1.2, 1.05, 0.9, 0.6], dtype=np.float32),
    np.array([900, 900, 900, 900, 940, 1000, 1000, 1050, 1050, 1050, 1100, 1100, 1100, 1100], dtype=np.float32),
    np.array([2300]*14, dtype=np.float32)
))
material_databas.append((  # Stål
    np.array([0, 20, 100, 120, 200, 300, 400, 500, 700, 750, 800, 1200], dtype=np.float32),
    np.array([55, 55, 50, 50, 47, 45, 40, 37, 30, 30, 27, 27], dtype=np.float32),
    np.array([500, 500, 500, 500, 500, 520, 600, 700, 1000, 5000, 800, 700], dtype=np.float32),
    np.array([7850]*12, dtype=np.float32)
))


