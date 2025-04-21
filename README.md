# Brandapp

## Beskrivning
Brandapp is finite element program developed in python, to simulate transient heat transfer inside solids exposed to fire.

## Installation
To runb the code:

1. Clone the repository:
   ```
   git clone git@github.com:emilnystr/Brandapp.git
   cd Brandapp
   ```


### The boundary conditions that are available are:
ISO 834:

$$ISO 834(t) = 20 + 345 \cdot \log_{10}\left(\frac{8t}{60} + 1\right) $$

HC180: 

$$HC180(t) = 20 + 1080 \left(1 - 0.325 e^{-0.167 t} - 0.675 e^{-2.5 t}\right)$$
