# Brandapp

## Description
Brandapp is finite element program developed in python, to simulate transient heat transfer inside solids exposed to fire.

## Installation
To run the code:

1. Clone the repository:
   ```
   git clone git@github.com:emilnystr/Brandapp.git
   ```

2. Install the Numba package:
   ```
   pip install numba
   ```


### The boundary conditions that are available are:
ISO 834 (option 1 in fire_curve):

$$ISO 834(t) = 20 + 345 \cdot \log_{10}\left(\frac{8t}{60} + 1\right) $$

HC180 (option 2 in fire_curve): 

$$HC180(t) = 20 + 1080 \left(1 - 0.325 e^{-0.167 t} - 0.675 e^{-2.5 t}\right)$$

Or the user have the option of using an automatically generated parametric fire curve based on the equations given in SS-EN 1991-1-2 Annex A (option 3 in fire_curve). The necessary input is specified in the config.json file. 

The user can also choose to have a constant surface temperature (option 4 in fire_curve)


## Default JSON configuration file

```json
{
    "simulation_time": 3600,
    "time_step": 0.5,
    "mm_per_layer": 5,
    "initial_temperature": 20,
    "Convective_heat_transfer_coefficient": 10,
    "ambient_temperature": 20,
    "emissivity": 0.8,
    "stefan_boltzmann_constant": 5.67e-8,
    "Fire_curve": 3,
    "Av": 31,
    "At": 500,
    "heq": 1.565,
    "b": 1849,
    "q_td": 340,
    "tillväxthastighet": 15
}
```
The temperature dependent material properties are built in inside the material.py file.

The default model is numerically stable for the current time step and spatial step, though the user must keep in mind that when using very small elements or/and having material with very high conductivity, the time step size may need to be decreased.
