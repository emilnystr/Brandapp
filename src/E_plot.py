import matplotlib.pyplot as plt
import numpy as np

def plot_results(element_sizes, T):
    x_pos = np.cumsum(np.concatenate([[0], element_sizes])*1000)
    plt.plot(x_pos, T)
    plt.xlabel("Avstånd [mm]")
    plt.ylabel("Temperatur (°C)")
    plt.title("Temperaturfördelning")
    plt.grid()
    plt.show()
    