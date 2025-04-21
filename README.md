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


### Brandtemperatur över tid
Ekvationen för brandtemperatur över tid är:
```latex
\begin{equation}
T_{fire}(t) = 20 + 345 \cdot \log_{10}\left(\frac{8t}{60} + 1\right)
\end{equation}
