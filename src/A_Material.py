import numpy as np

# Definiera dtype för strukturerad materialdata
material_dtype = np.dtype([
    ("temperatur", np.float32, (14,)),
    ("värmeledning", np.float32, (14,)),
    ("specifik_värmekapacitet", np.float32, (14,)),
    ("densitet", np.float32, (14,))
])

# Skapa materialdatabas med sammanhängande struktur
material_databas = np.array([
    (np.array([0, 20, 100, 101, 120, 121, 200, 250, 300, 350, 400, 500, 600, 1200], dtype=np.float32),
     np.array([2, 2, 1.75, 1.75, 1.7, 1.7, 1.55, 1.5, 1.35, 1.3, 1.2, 1.05, 0.9, 0.6], dtype=np.float32),
     np.array([900, 900, 900, 900, 940, 1000, 1000, 1050, 1050, 1050, 1100, 1100, 1100, 1100], dtype=np.float32),
     np.array([2300]*14, dtype=np.float32)),

    (np.array([0, 20, 100, 120, 200, 300, 400, 500, 700, 750, 800, 1200, 1400, 1400], dtype=np.float32),
     np.array([55, 55, 50, 50, 47, 45, 40, 37, 30, 30, 27, 27, 27, 27], dtype=np.float32),
     np.array([500, 500, 500, 500, 500, 520, 600, 700, 1000, 5000, 800, 700, 700, 700], dtype=np.float32),
     np.array([7850]*14, dtype=np.float32)),

    (np.array([0, 20, 100, 101, 120, 121, 200, 300, 500, 800, 1200, 1400, 1400, 1400], dtype=np.float32),
     np.array([0.12, 0.3, 0.13, 0.13, 0.13, 0.13, 0.15, 0.07, 0.09, 0.35, 1.5, 1.5, 1.5, 1.5], dtype=np.float32),
     np.array([1000, 1530, 1770, 13600, 13500, 2120, 1200, 1400, 1600, 1650, 1650, 1650, 1650, 1650], dtype=np.float32),
     np.array([504, 504, 504, 504, 450, 450, 450, 418, 342, 234, 171, 157, 126, 126], dtype=np.float32))
], dtype=material_dtype)