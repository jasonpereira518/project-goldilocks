# Project: Goldilocks

This project explores **exoplanet data** from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) through three complementary tools:  

1. **Exoplanet Habitability Explorer** — assigns "Goldilocks Scores" and visualizes planets in a Plotly dashboard.  
2. **OrbitNotes (Streamlit App)** — generates engaging, scientifically grounded exoplanet descriptions using OpenAI + LangChain.  
3. **Rogue Planet Detection** — identifies unusual planets using statistical outlier analysis.  

Together, these tools highlight *where life might exist*, *how to describe it*, and *which planets are anomalies worth studying further*.  

---

## 🚀 Features

### 🟢 Exoplanet Habitability Explorer
- Computes **Goldilocks Score** (0–100) based on:
  - Habitable Zone distance  
  - Planet size (Earth-like preferred)  
  - Orbital eccentricity  
  - Host star similarity to the Sun  
- Categorizes planets into:
  - `"Just Right"` 🌍
  - `"Borderline"` ⚠️
  - `"Too Cold/Hot"` ❄️🔥  
- Interactive **Plotly visualization** with:
  - Log-scale distance axis  
  - Custom scoring bands (Highly Habitable, Marginally Habitable)  
  - Solar System planets as references ⭐  
  - Exportable interactive HTML  

---

### ✨ OrbitNotes (Streamlit App)
- **Planet Selector**: Pick from real NASA exoplanets.  
- **Habitability Analysis**: Computes HZ bounds and classifies habitability.  
- **AI Narration**: Uses GPT-4o-mini to generate 30–70 word planet descriptions.  
- **Sidebar Controls**:
  - LLM parameters (temperature, tokens, penalties)  
  - Science filters (habitability strictness, planet size)  
- Expandable **Planet Profile** for raw data.  
- Polished UI with logo, metrics, and descriptions.  

---

### 🪐 Rogue Planet Detection
- Identifies **statistical outliers** in exoplanet properties using **z-scores**.  
- Flags planets with unusual:
  - Orbital distance  
  - Period  
  - Stellar/planetary properties  
- Exports unique outliers to `rogue_planets.csv` for further study.  

---

## 🛠️ Tech Stack

- [Pandas](https://pandas.pydata.org/) — data wrangling  
- [NumPy](https://numpy.org/) — scientific computation  
- [Plotly](https://plotly.com/python/) — interactive visualizations  
- [Streamlit](https://streamlit.io/) — web app interface  
- [LangChain](https://langchain.com/) — LLM orchestration  
- [OpenAI GPT-4o-mini](https://openai.com/research/gpt-4o) — narrative generation  
- [dotenv](https://pypi.org/project/python-dotenv/) — environment variable management  
- [Pillow](https://python-pillow.org/) — image handling  

---

## 📊 Data Sources

- **NASA Exoplanet Archive CSVs** (provided in repo or downloadable directly)  
  - `CDC Data - Narrow Data.csv`  
  - `PS_2025.09.20_08.00.03.csv`  
  - `cdcdata.csv`  

---

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/exoplanet-explorer.git
cd exoplanet-explorer
