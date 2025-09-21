# OrbitNotes 🌍✨

**OrbitNotes** is an interactive [Streamlit](https://streamlit.io/) application that combines real exoplanet data with AI-powered narration to generate engaging, scientifically accurate planet descriptions. It’s inspired by the “Goldilocks Zone” idea — finding worlds that are *too hot*, *too cold*, or *just right*.

---

## 🚀 Features

- **Planet Selector**: Choose from real exoplanets listed in the NASA Exoplanet Archive dataset.  
- **Habitability Analysis**:  
  - Computes host star luminosity.  
  - Estimates the inner and outer edges of the habitable zone (HZ).  
  - Classifies a planet as **Too Hot**, **Too Cold**, or **Just Right**.  
- **Planet Profiles**: Displays orbital, stellar, and planetary properties side-by-side.  
- **AI Narration**: Uses OpenAI’s GPT-4o-mini to generate a 30–70 word description of each planet.  
- **Custom Controls** (via sidebar):  
  - Adjust **temperature**, **max tokens**, and **frequency penalty** for LLM output.  
  - Tune **detail level**, **habitability strictness**, and **preferred planet size** filters.  
- **Expandable Details**: See the raw profile sent to the LLM.  
- **Polished UI**: Logo, sidebar settings, metrics, expandable sections, and more.  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — web interface  
- [LangChain](https://langchain.com/) — LLM orchestration  
- [OpenAI GPT-4o-mini](https://openai.com/research/gpt-4o) — text generation  
- [Pandas](https://pandas.pydata.org/) — data handling  
- [NumPy](https://numpy.org/) — scientific calculations  
- [Pillow](https://python-pillow.org/) — image handling  

---

## 📊 Data Source

- [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)  
- Example CSV file included: `PS_2025.09.20_08.00.03.csv`

---

## ⚙️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/orbitnotes.git
cd orbitnotes
