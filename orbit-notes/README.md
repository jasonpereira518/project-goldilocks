# orbit-notes

OrbitNotes 🌍✨

OrbitNotes is an interactive Streamlit
 application that combines real exoplanet data with AI-powered narration to generate engaging, scientifically accurate planet descriptions. It’s inspired by the “Goldilocks Zone” idea — finding worlds that are too hot, too cold, or just right.

🚀 Features

Planet Selector: Choose from real exoplanets listed in the NASA Exoplanet Archive dataset.

Habitability Analysis:

Computes host star luminosity.

Estimates the inner and outer edges of the habitable zone (HZ).

Classifies a planet as Too Hot, Too Cold, or Just Right.

Planet Profiles: Displays orbital, stellar, and planetary properties side-by-side.

AI Narration: Uses OpenAI’s GPT-4o-mini to generate a 30–70 word description of each planet.

Custom Controls (via sidebar):

Adjust temperature, max tokens, and frequency penalty for LLM output.

Tune detail level, habitability strictness, and preferred planet size filters.

Expandable Details: See the raw profile sent to the LLM.

Polished UI: Logo, sidebar settings, metrics, expandable sections, and more.

🛠️ Tech Stack

Streamlit
 — web interface

LangChain
 — LLM orchestration

OpenAI GPT-4o-mini
 — text generation

Pandas
 — data handling

NumPy
 — scientific calculations

Pillow
 — image handling

📊 Data Source

NASA Exoplanet Archive

Example CSV file included: PS_2025.09.20_08.00.03.csv

⚙️ Setup
1. Clone the Repository
git clone https://github.com/yourusername/orbitnotes.git
cd orbitnotes

2. Create a Virtual Environment (recommended)
python3 -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root with:

OPENAI_API_KEY=your_openai_api_key_here

5. Run the App
streamlit run app.py

📂 Project Structure
.
├── app.py                      # Main Streamlit application
├── favicon.png                 # Logo for app & browser tab
├── PS_2025.09.20_08.00.03.csv  # NASA exoplanet dataset
├── requirements.txt            # Python dependencies
└── README.md                   # This file

🧭 Usage

Launch the app and select a planet (e.g., Kepler-22 b).

Explore its orbit, host star, and habitability analysis.

Adjust sidebar controls for narration and filters.

Click Generate Description to get an AI-generated narrative.

⚠️ Notes

This is a demo hackathon project — do not use outputs as authoritative scientific references.

Some planets may have missing or incomplete data. The AI will acknowledge uncertainty.

Ensure your .env is not committed to version control.

📜 License

MIT License. Feel free to fork, remix, and build upon OrbitNotes.
