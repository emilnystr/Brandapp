import numpy as np
import time
import json
from A_Material import material_databas
from B_Input import skapa_indata
from C_FEM import skapa_element
from D_FemCalc import*
from E_plot import plot_results
from Parametrisk_brandkurva import*

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

materialdata = skapa_indata()
element_sizes, element_material_indices, antal_noder = skapa_element(materialdata)

initial_temperature = config["initial_temperature"]
simuleringstid = config["simulation_time"]
h = config["Convective_heat_transfer_coefficient"]
T_g = config["ambient_temperature"]
sigma = config["stefan_boltzmann_constant"]
epsilon = config["emissivity"]
dt = config["time_step"]
brandkurva = config["Fire_curve"]
Constant_surface_temperature = config["constant_surface_temperature"]

T = np.full(antal_noder, initial_temperature, dtype=np.float32)
Q = np.zeros(antal_noder, dtype=np.float32)
antal_tidssteg = int(simuleringstid / dt)

# Beräknar hur ofta vi ska uppdatera status (var 1%)
uppdatera_tid = max(1, antal_tidssteg // 50)

start_time = time.time()
for i in range(antal_tidssteg):
    tid = i * dt

    if brandkurva == 1:
        T_fire = iso_brandkurva(tid)
    elif brandkurva == 2:
        T_fire = HC180(tid)
    elif brandkurva == 3:
        T_fire = parametrisk_brand(tid)
    elif brandkurva == 4:
        T_fire = Constant_surface_temperature
    else:
        print("du har angett en felaktig brandkurva")
    
    K, C = beräkna_matriser(element_sizes, element_material_indices, material_databas, T)
    
    Q[0] = h * (T_fire - T[0]) + sigma * epsilon * ((T_fire + 273.15)**4 - (T[0] + 273.15)**4)
    Q[-1] = h * (T_g - T[-1]) + sigma * epsilon * ((T_g + 273.15)**4 - (T[-1] + 273.15)**4)
    
    T += dt * (Q - K @ T) / C
    
    #framstegsindikatorn
    if i % uppdatera_tid == 0 or i == antal_tidssteg - 1:
        procent_klar = (i + 1) / antal_tidssteg * 100
        print(f"\rSimuleringen är {procent_klar:.1f}% klar", end="", flush=True)

print(f"\nSimuleringen tog {time.time() - start_time:.2f} sekunder")

plot_results(element_sizes, T)
print(T)