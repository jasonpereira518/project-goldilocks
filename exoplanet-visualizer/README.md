# 🌌 Exoplanet Habitability Explorer

An interactive visualization tool for exploring potentially habitable exoplanets using NASA's Exoplanet Archive data.

## 🚀 Features

- **Habitability Scoring**: Custom 0-100 algorithm based on Kopparapu Habitable Zone model
- **Interactive Visualization**: 36,000+ exoplanets with zoom, hover, and filtering
- **Solar System Reference**: Earth, Mars, Jupiter, Saturn, and Neptune for comparison
- **Scientific Accuracy**: Multi-parameter analysis including orbital stability and star similarity

## 📊 Technology Stack

- **Python 3.x**
- **Pandas** - Data manipulation
- **NumPy** - Mathematical computations
- **Plotly** - Interactive visualizations

## 🔧 Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/sainag7/exoplanet-explorer.git
cd exoplanet-explorer
```

2. Install dependencies:
```bash
pip install pandas numpy plotly
```

3. Run the visualization:
```bash
python main.py
```

## 📈 Results

- **17,585** highly habitable planets (score ≥ 85)
- **197** marginally habitable planets (60-84)
- **18,370** unlikely habitable planets (< 60)
- **Closest habitable planet**: 1.30 parsecs from Earth

## 🔬 Scientific Methodology

### Habitability Scoring Algorithm (0-100 Scale)

**Base Scoring - Habitable Zone Position:**
- Uses Kopparapu Habitable Zone Model (2013)
- Calculates star luminosity: `L_star = (R_star²) × (T_star/5778)⁴`
- **In HZ**: 50-85 points based on proximity to zone center
- **Outside HZ**: 5-49 points based on distance from boundaries

**Multi-Factor Analysis:**
- **Planet Size** (±25 points): Optimal Earth-like radius (0.8-1.4 Earth radii)
- **Orbital Stability** (±8 points): Circular orbits preferred (eccentricity < 0.05)
- **Star Similarity** (±8 points): Sun-like temperature (5778K ± 5%)

### Classification Categories
- **🌍 "Just Right"**: Score ≥ 85 (Highly habitable)
- **⚠️ "Borderline"**: Score 60-84 (Marginally habitable)  
- **🔥❄️ "Too Cold/Hot"**: Score < 60 (Unlikely habitable)

## 📊 Data Source

NASA Exoplanet Archive - Planetary Systems Composite Data
- **36,152 planets analyzed** (after quality filtering)
- Updated with latest confirmed exoplanet discoveries

## 🎨 Visualization Features

- **Interactive scatter plot** with logarithmic distance scaling
- **Solar system reference planets** (Earth, Mars, Jupiter, Saturn, Neptune)
- **Custom hover tooltips** with detailed planet parameters
- **Color-coded habitability categories**
- **Professional dark space theme**
- **Export to HTML** functionality

## 📸 Example Output

The visualization generates an interactive plot showing:
- X-axis: Distance from Earth (parsecs, log scale)
- Y-axis: Goldilocks Habitability Score (0-100)
- Colors: Habitability categories
- Reference: Solar system planets as star markers

## 🤝 Contributing

Feel free to contribute by:
1. Forking the repository
2. Creating a feature branch
3. Making your improvements
4. Submitting a pull request

## 📄 License

This project is open source and available under the MIT License.