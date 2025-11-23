# Lorenz80 🌪️

## 📝 Description

This repository contains an implementation and study of the Lorenz 1980 model (Lorenz-80), 
originally introduced by E. D. Lorenz in his 1980 paper:
*[Attractor Sets and Quasi-Geostrophic Equilibrium](
https://journals.ametsoc.org/view/journals/atsc/37/8/1520-0469_1980_037_1685_asaqge_2_0_co_2.xml)*

In this same article, Lorenz also presents the PE (Primitive Equations) model and the QG (Quasi-Geostrophic) model, 
from which the Lorenz-80 formulation is derived as a simplified low-order representation.

It also includes an implementation of the BE model (Balance equations) from: *[“Intermediate Model Solutions to the Lorenz Equations: Strange Attractors and Other Phenomena”](
https://journals.ametsoc.org/view/journals/atsc/39/1/1520-0469_1982_039_0003_imsttl_2_0_co_2.xml)* with adaptations from *[“Stochastic rectification of fast oscillations on slow manifold closures”](
https://www.pnas.org/doi/10.1073/pnas.2113650118)*

This repository includes:

- Implementation of the Lorenz-1980 model
- Implementation of the BE model
- Deterministic simulations and visualizations
- Time series, attractors, and sensitivity experiments
- CSV export utilities and scientific figures

## ⚙️ Installation

1. Clone the repository.
   ```bash
   git clone https://github.com/lucasamtaylor01/Lorenz80.git
   ```
2. Install the dependencies.
3. 
   **Linux/macOS:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
   **Windows (CMD)**
   ```bash
   python -m venv .venv && .venv\Scripts\activate.bat && pip install -r requirements.txt
   ```
4. Run `main.py`

## 🤝 Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request via GitHub if you have suggestions, improvements, or feedback.

## 📄 License
This project is currently licensed under the [MIT License](LICENSE).

## 🤖 Good Use of AI
This project was developed with the assistance of [GitHub Copilot](https://github.com/features/copilot).

