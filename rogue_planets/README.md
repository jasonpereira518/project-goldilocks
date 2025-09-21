# Rogue Planet Detector

This project processes **exoplanet data** from a CSV file to detect potential *rogue planets*—planets with unusual orbital or stellar properties compared to the overall dataset. It uses statistical analysis to identify outliers and outputs a list of unique planet names that deviate significantly from the expected ranges.

---

## 📌 Features
- Loads exoplanet data from `cdcdata.csv`.
- Selects key astrophysical features for analysis:
  - `pl_name` (Planet Name)  
  - `pl_orbsmax` (Orbital Semi-Major Axis, AU)  
  - `pl_orbper` (Orbital Period, days)  
  - `st_teff` (Stellar Effective Temperature, K)  
  - `st_rad` (Stellar Radius, Solar radii)  
  - `st_mass` (Stellar Mass, Solar masses)  
  - `pl_rade` (Planet Radius, Earth radii)  
- Cleans missing data.  
- Standardizes data and computes **z-scores**.  
- Flags planets as outliers if any feature has |z| > 3.  
- Ensures only unique planets are saved.  
- Exports the results into `rogue_planets.csv`.

---

## ⚙️ Installation
Make sure you have **Python 3.8+** installed. Install required dependencies:

```bash
pip install pandas numpy
