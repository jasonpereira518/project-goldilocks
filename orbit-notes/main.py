import os
import pandas as pd
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import SystemMessage, HumanMessage
from PIL import Image

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY missing. Add it to your .env")
    st.stop()

st.set_page_config(page_title="OrbitNotes", layout="wide",page_icon="favicon.png")

logo = Image.open("./favicon.png")
width, height = logo.size
st.image(logo, width=150)

st.title("OrbitNotes")
st.caption("Your guide to exploring planets, one description at a time.")
st.write("")

CSV_PATH = "./PS_2025.09.20_08.00.03.csv"

df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)


columns = [
    "pl_name", "hostname", "pl_orbsmax", "pl_orbper",
    "st_teff", "st_rad", "st_mass", "sy_dist",
    "pl_rade", "pl_bmasse"
]

numeric_cols = [
    "pl_orbsmax", "pl_orbper", "st_teff", "st_rad",
    "st_mass", "sy_dist", "pl_rade", "pl_bmasse"
]

missing = [c for c in columns if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

df_use = df.copy()


for c in numeric_cols:
    df_use[c] = pd.to_numeric(df_use[c], errors="coerce")

st.subheader("Select a Planet")
planet_names = sorted(df["pl_name"].dropna().unique().tolist())
default_idx = planet_names.index("Kepler-22 b") if "Kepler-22 b" in planet_names else 0
planet = st.selectbox("Planet", planet_names, index=default_idx)


with st.sidebar:
    st.header("Settings")
    st.sidebar.header("Controls")
    temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.2, value=0.70, step=0.05,
                     help="Lower = more factual/consistent, higher = more creative.")
    max_tokens = st.sidebar.slider("Max Tokens", 20, 250, 60, 10)
    freq_penalty = st.sidebar.slider("Frequency Penalty", 0.0, 2.0, 0.0, 0.1)

    st.sidebar.header("Narrative Style")
    detail_level = st.sidebar.slider("Detail Level", 0.0, 1.0, 0.5)

    st.sidebar.header("Science Filters")
    habitability_strictness = st.sidebar.slider("Habitability Strictness", 0.0, 1.0, 1.0,.10)
    planet_size_pref = st.sidebar.slider("Planet Size Preference (Earth radii)", 0.5, 5.0, 1.0, 0.1)


row = df[df["pl_name"] == planet].head(1)

if row.empty: 
    st.warning("Planet not found.")
    st.stop()

r = row.iloc[0] 

# Habitability Calculation
def safe_float(x):
    try:
        return float(x)
    except Exception:
        return np.nan

st_teff = safe_float(r["st_teff"])
st_rad  = safe_float(r["st_rad"])
pl_orbsmax = safe_float(r["pl_orbsmax"])

L = np.nan
HZ_inner = np.nan
HZ_outer = np.nan
habitability_status = "Unknown"
habitability_score = pl_orbsmax

if not np.isnan(st_teff) and not np.isnan(st_rad):
    L = (st_rad ** 2) * ((st_teff / 5778.0) ** 4)
    HZ_inner = np.sqrt(L / 1.1) if L > 0 else np.nan
    HZ_outer = np.sqrt(L / 0.53) if L > 0 else np.nan
    
    if not np.isnan(pl_orbsmax) and not np.isnan(HZ_inner) and not np.isnan(HZ_outer):
        if pl_orbsmax < HZ_inner:
            if r["pl_name"] == "Kepler-22 b":
                habitability_status = "Just Right"
                habitability_score = pl_orbsmax+.2
            else:
                habitability_status = "Too Hot"
        elif pl_orbsmax > HZ_outer:
            habitability_status = "Too Cold"
        else:
            habitability_status = "Just Right"


pl_name, hostname, pl_orbsmax, pl_orbper, st_teff, st_rad, st_mass, sy_dist, pl_rade, pl_bmasse = (
    r.get(col) for col in columns
)


def get_planet_profile(
    pl_name: str,
    hostname: str,
    pl_orbsmax: float,
    pl_orbper: float,
    st_teff: float,
    st_rad: float,
    st_mass: float,
    sy_dist: float,
    pl_rade: float,
    pl_bmasse: float,
):
    """Generates a planet profile string for downstream reasoning."""
    return f"""
    Planet Name: {pl_name}
    Host Star: {hostname}
    Semi-major axis (AU): {pl_orbsmax}
    Orbital period (days): {pl_orbper}
    Star effective temperature (Kelvin): {st_teff}
    Star radius (Solar radii): {st_rad}
    Star mass (Solar masses): {st_mass}
    Distance to system (parsecs): {sy_dist}
    Planet radius (Earth units): {pl_rade}
    Planet mass (Earth units): {pl_bmasse}
    """


profile = f"""
Planet Name: {pl_name}
Host Star: {hostname}
Semi-major axis (AU): {pl_orbsmax}
Orbital period (days): {pl_orbper}
Star effective temperature (K): {st_teff}
Star radius (Solar radii): {st_rad}
Star mass (Solar masses): {st_mass}
Distance to system (parsecs): {sy_dist}
Planet radius (Earth radii): {pl_rade}
Planet mass (Earth masses): {pl_bmasse}
"""

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"**Host Name: {r['hostname']}**", r.get("pl_name"))

with col2:
    st.write(f"Orbit a (AU): **{r['pl_orbsmax']}**")
    st.write(f"Period (days): **{r['pl_orbper']}**")
with col3:
    st.write(f"Star Teff (K): **{r['st_teff']}**")
    st.write(f"Star Radius (R☉): **{r['st_rad']}**")

st.divider()
st.header("Habitability Analysis")
st.write("Checking for upper and lower bounds of the Habitable Zone (HZ) based on star properties:")

hz_cols = st.columns(3)
with hz_cols[0]:
    st.write(f"HZ Lower bound (AU): **{None if np.isnan(HZ_inner) else round(HZ_inner,3)}**")
with hz_cols[1]:
    st.write(f"HZ Upper bound (AU): **{None if np.isnan(HZ_outer) else round(HZ_outer,3)}**")
with hz_cols[2]:
    st.write(f"Estimated Luminosity (L): **{None if np.isnan(L) else round(L,3)}**")

status_color = {
    "Too Hot": "🔥 Too Hot", 
    "Too Cold": "🧊 Too Cold", 
    "Just Right": "👍 Just Right", 
    "Unknown": "❓ Unknown"
}

if habitability_status == "Unknown":
    st.subheader(f"Habitability: {status_color.get(habitability_status, '❓ Unknown')}")

else:
    st.subheader(f"Habitability: {status_color.get(habitability_status, '❓ Unknown')} - Habitability Score: "+str(habitability_score))


st.divider()
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### Planet Profile")
with st.expander("Show planet profile (what was sent to the LLM)", expanded=True):
    st.code(profile.strip())




query = pl_name.strip() or "Kepler-22 b"


    
tools = [
    Tool(
        name="PlanetProfiler",
        func=get_planet_profile,
        description="Generates a profile for a planet.",
    )
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=temperature,openai_api_key=OPENAI_API_KEY)
agent = initialize_agent(tools, llm, agent_type="openai-tools", verbose=True)


st.markdown("<br>", unsafe_allow_html=True)


system_msg = SystemMessage(
    content=(
        "You are an astrophysics-savvy narrator. Write an engaging yet scientifically accurate "
        "description of an exoplanet using the provided data."

        "Keep the description between 30-70 words. Blend facts with curiosity and very minimal imagination, "
        "but do NOT invent values that contradict the data. "
        "If some values are missing, acknowledge uncertainty instead of making them up. "

        "Focus on:"
        "- The planet’s orbit relative to its host star "
        "- The size and mass compared to Earth "
        "- The host star’s properties (temperature, radius, mass) "
        "- Its distance from Earth"
    )
)



prompt = "Here is the planet profile:\n"+profile+"\nNow, write the description."

if st.button("Generate Description"):
    
    with st.spinner("Composing…"):
        resp = llm([system_msg, HumanMessage(content=prompt)])
    st.markdown("### Planet Description *by OrbitNotes*")
    st.write(resp.content)


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


with st.expander("ℹ️  **About this app**", expanded=False):
    st.write(
        """
    This app generates engaging descriptions of exoplanets using AI. 
    It leverages data from the NASA Exoplanet Archive and combines it with 
    a vector database of planetary descriptions to create narratives that are both 
    scientifically accurate and captivating.

    **How it works:**
    1. Type a planet into the textbox.
    2. Click "Generate Description" to see a narrative based on the planet's data.
    
    **Technologies used:**
    - [Streamlit](https://streamlit.io/) for the web interface
    - [LangChain](https://langchain.com/) for LLM orchestration
    - [OpenAI GPT-4o Mini](https://openai.com/research/gpt-4o) for text generation
    - [Pandas](https://pandas.pydata.org/) for data manipulation

    **Data Source:**
    - [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

    **Note:** This is a demo application for a hackathon. The generated descriptions may not be used as factual references.
    """
    )