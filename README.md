Here's the updated and consolidated README.md file that aligns with your theory:

```markdown
# Brandapp: 1D Finite Element Heat Transfer Simulation for Fire Analysis

## Introduction
Brandapp is a Python-based finite element program for simulating transient heat transfer in solids exposed to fire. The application solves the heat conduction equation in multi-layered materials with temperature-dependent properties using the Finite Element Method (FEM).

**Key Features**:
- Dynamic spatial discretization for varying material thicknesses
- Multiple fire curve options (ISO 834, HC180, parametric)
- Numba-accelerated computations
- Temperature-dependent material properties

**Note**: This 1D model cannot analyze complex geometries - users must carefully assess simplifications.

## Theory

### Governing Equations
The core partial differential equation solved:

```math
\rho(T)c_p(T)\frac{\partial T}{\partial t} = \nabla\cdot(k(T)\nabla T) + Q
```

### Finite Element Formulation
The energy balance equation is constructed as:

```math
\overline{C} \frac{d\overline{T}}{dt} + \overline{K}\overline{T} = \overline{Q}
```

With explicit time stepping:

```math
\overline{T}^{j+1} = {T}^{j} + dt \cdot \overline{C}^{-1}(\overline{Q}^{j} - \overline{K} \cdot \overline{T}^{j})
```

### Boundary Conditions
Heat flux at surfaces combines convection and radiation:

```math
q'' = h(T_\infty - T_s) + \sigma\epsilon(T_\infty^4 - T_s^4)
```

## Fire Curve Options

1. **ISO 834 Standard Curve**:
   ```math
   T(t) = 20 + 345 \cdot \log_{10}\left(\frac{8t}{60} + 1\right)
   ```

2. **HC180 Hydrocarbon Curve**:
   ```math
   T(t) = 20 + 1080 \left(1 - 0.325 e^{-0.167 t} - 0.675 e^{-2.5 t}\right)
   ```

3. **Parametric Fire Curve** (SS-EN 1991-1-2 Annex A)
   - Automatically generated based on config.json parameters

4. **Constant Temperature** (User-defined)

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:emilnystr/Brandapp.git
   ```

2. Install required packages:
   ```bash
   pip install numba numpy matplotlib
   ```

## Configuration

Default `config.json` parameters:

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
    "growth_rate": 15
}
```

## Numerical Considerations
- Default settings are numerically stable for most cases
- Smaller elements or high conductivity materials may require reduced time steps
- Temperature-dependent properties are defined in `material.py`

## Usage
1. Configure settings in `config.json`
2. Define material properties in `material.py`
3. Run simulation:
   ```bash
   python main.py
   ```
4. Analyze results (temperature profiles are automatically plotted)

## License
MIT License
```

Key improvements:
1. Consolidated all theory sections into one coherent flow
2. Organized fire curve equations clearly
3. Added complete installation instructions
4. Structured configuration details
5. Added practical usage instructions
6. Maintained all mathematical formulations
7. Kept important notes about numerical stability

The file is now ready to copy and paste directly into your README.md - all formatting will be preserved.