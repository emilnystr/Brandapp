import numpy as np
from numba import njit
import math
from Parametrisk_brandkurva import*

@njit
def iso_brandkurva(tid):
    return 20 + 345 * np.log10(8 * tid / 60 + 1) #standardbrandkurva

@njit
def HC180(tid):
    return 20 + 1080 * (1 - 0.325 * math.exp(-0.167 * tid) - 0.675 * math.exp(-2.5 * tid)) #kolvätekurva




@njit
def linjär_interpolering(temperaturer, värden, T):
    n = len(temperaturer)
    if T <= temperaturer[0]: return värden[0]
    if T >= temperaturer[-1]: return värden[-1]
    for i in range(n-1):
        if temperaturer[i] <= T < temperaturer[i+1]:
            x = (T - temperaturer[i]) / (temperaturer[i+1] - temperaturer[i])
            return värden[i] + x * (värden[i+1] - värden[i])
    return värden[-1]

@njit
def beräkna_matriser(element_sizes, element_material_indices, material_databas, T):
    n = len(T)
    K = np.zeros((n, n), dtype=np.float32)
    C = np.zeros(n, dtype=np.float32)

    for i in range(len(element_sizes)):
        dx = element_sizes[i]
        mat_idx = element_material_indices[i]
        
        T_avg = (T[i] + T[i+1]) / 2
        
        # Hämta materialdata direkt från strukturerad NumPy-array
        temp = material_databas[mat_idx][0]
        k_vals = material_databas[mat_idx][1]
        c_vals = material_databas[mat_idx][2]
        rho_vals = material_databas[mat_idx][3]
        
        k = linjär_interpolering(temp, k_vals, T_avg)
        c = linjär_interpolering(temp, c_vals, T_avg)
        rho = linjär_interpolering(temp, rho_vals, T_avg)
    
        # Uppdatera styvhetsmatrisen K
        K[i, i] += k/dx
        K[i, i+1] -= k/dx
        K[i+1, i] -= k/dx
        K[i+1, i+1] += k/dx
        
        # Uppdatera värmekapacitetsvektorn C
        C_val = rho * c * dx / 2
        C[i] += C_val
        C[i+1] += C_val
        
    return K, C