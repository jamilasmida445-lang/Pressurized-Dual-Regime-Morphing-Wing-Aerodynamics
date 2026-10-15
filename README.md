# Hybrid Dual-Regime Pneumatic Morphing Wing: CFD Validation Dataset

## Overview
This repository contains the complete computational fluid dynamics (CFD) dataset, simulation cases, and analysis scripts for the **Hybrid Dual-Regime Pneumatic Morphing Wing** project. 

The study evaluates an aerodynamic proof-of-concept across an extreme flight envelope from **Mach 0.15 to Mach 2.5**, utilizing active pneumatic pressure differentials ($\Delta P$) to shift between an inflated supercritical profile ($M < 1.0$) and a collapsed biconvex profile ($M \ge 1.0$).

---

## Repository Structure

```text
├── my_Cases/                     <-- Contains all 43 OpenFOAM simulation directories
│   ├── morphicwing01_M0p15_AoAneg4/morphicwing01_M0p15_AoAneg4/  (Subsonic nested structure)
│   ├── ...
│   └── morphicwing30_M1p00_AoA0/new/                             (Supersonic nested structure)
├── aerodynamic_results_summary.csv     <-- Maximum L/D summary across Mach numbers
└── aerodynamic_results_analyzed_clean.csv <-- Full processed dataset (43 cases with forces, moments, and standard deviations)
Elkateb, Y. Y. T. (2026). Hybrid Dual-Regime Pneumatic Morphing Wing: A Computational Fluid Dynamics Proof-of-Concept Across Mach 0.15 to 2.5. engrXiv.
