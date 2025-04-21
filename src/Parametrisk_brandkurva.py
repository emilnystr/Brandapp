import json
import math
import matplotlib.pyplot as plt
import numpy as np
from numba import njit

def parametrisk_kurva():
    with open("config.json", 'r') as f:
        cfg = json.load(f)

    # Läs parametrar
    tillväxt = 15  # tillfälligt värde
    Av = cfg["Av"]
    At = cfg["At"]
    heq = cfg["heq"]
    b = cfg["b"]
    q_td = cfg["q_td"]
    t_lim = tillväxt / 60

    # Beräkna O och kontrollera giltighet
    O = (Av * math.sqrt(heq)) / At
    if not 0.02 <= O <= 0.20:
        raise ValueError(f"Ogiltigt O-värde: {O:.3f}. Måste vara mellan 0.02 och 0.20")
    if not 100 <= b <= 2200:
        raise ValueError(f"Ogiltigt b-värde: {b:.1f}. Måste vara mellan 100 och 2200")

    # Beräkningar
    Gamma = ((O / b) ** 2) / ((0.04 / 1160) ** 2)
    t_max_temp = 0.2e-3 * q_td / O
    t_max = max(t_max_temp, t_lim)
    t_star_max = t_max * Gamma

    # Temperatur vid t_max
    T_max = 20 + 1325 * (
        1 - 0.324 * math.exp(-0.2 * t_star_max)
        - 0.204 * math.exp(-1.7 * t_star_max)
        - 0.472 * math.exp(-19 * t_star_max)
    )

    # Avkylningsfaktor
    x = 1.0 if t_max_temp > t_lim else (t_lim * Gamma / t_star_max)

    # Simuleringstider (sekunder)
    simuleringstid = 10**4  # gräns
    tider = []
    temperaturer = []
    O_lim = (0.1e-3 * q_td) / t_lim
    Gamma_lim = ((O_lim / b) ** 2) / ((0.04 / 1160) ** 2)
    
    t = 0
    while t <= simuleringstid:
        t_h = t / 3600  # timmar
        if t_max == t_lim:
            t_star = t * Gamma_lim / 3600
        else:
            t_star = t_h * Gamma

        if t_h <= t_max:
            # Uppvärmningsfas
            T = 20 + 1325 * (
                1 - 0.324 * math.exp(-0.2 * t_star)
                - 0.204 * math.exp(-1.7 * t_star)
                - 0.472 * math.exp(-19 * t_star)
            )
        else:
            # Avsvalningsfas
            if t_star_max <= 0.5:
                T = T_max - 625 * (t_star - t_star_max)
            elif t_star_max < 2:
                T = T_max - 250 * (3 - t_star_max) * (t_star - t_star_max * x)
            else:
                T = T_max - 250 * (t_star - t_star_max)
            T = max(T, 20)

        tider.append(t_h)
        temperaturer.append(T)

        #avbryt loopen när temperaturen når 20 under avsvalning
        if t_h > t_max and T == 20:
            break

        t += 1  # öka med 1 sekund

    return tider, temperaturer, t_max, cfg


# Hämta den parametriska brandkurvans data
tider_hours, temperaturer, t_max, cfg = parametrisk_kurva()

# Konvertera till NumPy-array för Numba
temperaturer_array = np.array(temperaturer, dtype=np.float32)

@njit
def parametrisk_brand(tid):
    if tid == 0:
        return 20.0
    n = len(temperaturer_array)
    if n == 0:
        return 20.0
    if tid >= n - 1:
        return temperaturer_array[-1]
    i = int(tid)
    x = tid - i
    return temperaturer_array[i] + x * (temperaturer_array[i+1] - temperaturer_array[i])

def plot_kurva(tider, temperaturer):
    minuter = [t * 60 for t in tider]
    plt.figure(figsize=(10, 6))
    plt.plot(minuter, temperaturer, 'r-', linewidth=2)

    
    plt.xlabel("Tid (minuter)", labelpad=10)
    plt.ylabel("Temperatur (°C)", labelpad=10)
    plt.grid(True, alpha=0.3)
    #plt.axvline(x=t_max * 60, color='blue', linestyle='--', label=f't_max = {t_max*60:.1f} min')
    plt.legend()
    plt.xlim(0, max(minuter[-1], 100))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    tider, temperaturer, t_max, config = parametrisk_kurva()
    plot_kurva(tider, temperaturer)
    print(temperaturer)