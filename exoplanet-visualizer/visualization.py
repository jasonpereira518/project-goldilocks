import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('CDC Data - Narrow Data.csv')

def classify_goldilocks(row):
    try:
        # Compute star luminosity 
        R_star = row["st_rad"]       
        T_star = row["st_teff"]      
        L_star = (R_star**2) * (T_star/5778.0)**4  # luminosity relative to Sun

        # --- Step 2: Compute habitable zone edges (AU) ---
        HZ_inner = np.sqrt(L_star / 1.1)
        HZ_outer = np.sqrt(L_star / 0.53)

        # --- Step 3: Get planet orbital distance ---
        a = row["pl_orbsmax"]  # semi-major axis in AU

        # --- Step 4: Calculate base score based on HZ position ---
        score = 0
        
        if HZ_inner <= a <= HZ_outer:
            # Planet is in habitable zone - calculate how centered it is
            HZ_center = (HZ_inner + HZ_outer) / 2
            HZ_width = HZ_outer - HZ_inner
            distance_from_center = abs(a - HZ_center)
            # Score 50-85 based on position in HZ (closer to center = higher)
            # Made more strict - perfect center gets 85, edges get 50
            position_score = 85 - (distance_from_center / HZ_width) * 35
            score = max(50, position_score)
        else:
            # Planet is outside HZ - calculate how far
            if a < HZ_inner:
                distance_ratio = a / HZ_inner
                # Too hot: score 5-49 based on how close to HZ
                score = 5 + (distance_ratio * 44)
            else:  # a > HZ_outer
                distance_ratio = HZ_outer / a
                # Too cold: score 5-49 based on how close to HZ
                score = 5 + (distance_ratio * 44)
        
        # --- Step 5: Adjust score based on planet size ---
        R_p = row["pl_rade"]  # planet radius in Earth radii
        if not pd.isna(R_p):
            if 0.8 <= R_p <= 1.4:
                # Perfect Earth-like size - maximum bonus (very strict)
                score += 15
            elif 0.6 <= R_p <= 1.8:
                # Good size - moderate bonus
                score += 8
            elif 0.5 <= R_p <= 2.0:
                # Acceptable size - small bonus
                score += 3
            elif R_p > 2.0:
                # Gas giant - penalty
                penalty = min(25, (R_p - 2.0) * 8)
                score -= penalty
            elif R_p < 0.5:
                # Too small - penalty
                penalty = (0.5 - R_p) * 25
                score -= penalty
        
        # --- Step 6: Additional factors for fine-tuning (more strict) ---
        # Orbital eccentricity (stricter requirements)
        if not pd.isna(row.get("pl_orbeccen")):
            ecc = row["pl_orbeccen"]
            if ecc < 0.05:
                score += 8  # Nearly circular orbit - big bonus
            elif ecc < 0.1:
                score += 4  # Very circular orbit - moderate bonus
            elif ecc < 0.2:
                score += 1  # Fairly circular - small bonus
            elif ecc > 0.3:
                score -= (ecc - 0.3) * 30  # High eccentricity - bigger penalty
        
        # Star temperature (prefer sun-like stars, stricter)
        if not pd.isna(T_star):
            temp_diff = abs(T_star - 5778) / 5778
            if temp_diff < 0.05:
                score += 8  # Very sun-like star - big bonus
            elif temp_diff < 0.1:
                score += 4  # Sun-like star - moderate bonus
            elif temp_diff < 0.2:
                score += 1  # Somewhat sun-like - small bonus
            elif temp_diff > 0.4:
                score -= temp_diff * 15  # Very different star - bigger penalty
        
        return max(0, min(100, score))
        
    except:
        return 0

# Create category mapping based on score ranges
def categorize_from_score(score):
    if score >= 85:
        return "\"Just Right\""
    elif score >= 60:
        return "\"Borderline\""
    else:
        return "\"Too Cold/Hot\""

# Apply the calculations
df["goldilocks_score"] = df.apply(classify_goldilocks, axis=1)
df["goldilocks_category"] = df["goldilocks_score"].apply(categorize_from_score)

# Filter out rows with missing essential data and create a clean dataset for plotting
plot_df = df.dropna(subset=['sy_dist', 'goldilocks_score']).copy()

# Remove outliers to make the graph cleaner
# Filter distance outliers (keep planets within reasonable distance range)
distance_q95 = plot_df['sy_dist'].quantile(0.95)  # 95th percentile
plot_df = plot_df[plot_df['sy_dist'] <= distance_q95]

# Filter out extreme distance values (very close planets that might be measurement errors)
plot_df = plot_df[plot_df['sy_dist'] >= 1.0]  # Keep planets at least 1 parsec away

# Create the enhanced scatter plot with uniform dot sizes
fig = px.scatter(
    plot_df,
    x="sy_dist",
    y="goldilocks_score",
    color="goldilocks_category",
    hover_name="pl_name",
    hover_data={
        "sy_dist": ":.2f",
        "pl_eqt": ":.1f",
        "pl_rade": ":.2f",
        "pl_masse": ":.2f",
        "st_teff": ":.0f",
        "goldilocks_score": ":.1f"
    },
    opacity=0.7,
    title="🌌 Exoplanet Habitability Explorer",
    labels={
        "sy_dist": "Distance from Earth (parsecs) ",
        "goldilocks_score": "Goldilocks Score ",
        "pl_eqt": "Equilibrium Temperature (K) ",
        "pl_rade": "Planet Radius (Earth radii) ",
        "pl_masse": "Planet Mass (Earth masses) ",
        "st_teff": "Star Temperature (K) ",
        "goldilocks_category": "Habitability Category "
    }
)

# Add Solar System planets for reference
solar_system_planets = {
    "🌍 Earth": {"distance": 0.00000, "score": 100, "color": "blue"},
    "🔴 Mars": {"distance": 0.000005848, "score": 65, "color": "red"},
    "🪐 Jupiter": {"distance": 0.000007848, "score": 15, "color": "orange"},
    "🪐 Saturn": {"distance": 0.000014848, "score": 12, "color": "gold"},
    "🌌 Neptune": {"distance": 0.000024848, "score": 8, "color": "darkblue"}
}

# Add each solar system planet as a separate trace
for planet_name, data in solar_system_planets.items():
    fig.add_trace(go.Scatter(
        x=[data["distance"]],
        y=[data["score"]],
        mode='markers+text',
        marker=dict(
            size=12,
            color=data["color"],
            symbol="star",
            line=dict(width=2, color="white")
        ),
        text=[planet_name],
        textposition="top center",
        textfont=dict(size=12, color="white"),
        name=f"Solar System: {planet_name}",
        showlegend=False,  # Remove from legend
        hovertemplate=f"<b>{planet_name}</b><br>" +
                     f"Distance: {data['distance']:.6f} parsecs<br>" +
                     f"Goldilocks Score: {data['score']}<br>" +
                     "<extra></extra>"
    ))

# Custom color scheme
color_map = {
    "\"Just Right\"": "#2E8B57",      # Sea green
    "\"Borderline\"": "#DAA520",      # Goldenrod
    "\"Too Cold/Hot\"": "#DC143C"   # Crimson
}

fig.for_each_trace(lambda t: t.update(
    marker_color=color_map.get(t.name, t.marker.color),
    marker_line_width=1,
    marker_line_color="white",
    marker_size=6  # Uniform dot size
))

# Enhanced layout with professional styling
fig.update_layout(
    title={
        'text': "🌌 Exoplanet Habitability Explorer<br><sub>Discover potentially habitable worlds across the galaxy</sub>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': 'white'}
    },
    xaxis_title="Distance from Earth (parsecs)",
    yaxis_title="Goldilocks Habitability Score (0–100)",
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0.9)',
    paper_bgcolor='rgba(0,0,0,0.9)',
    font=dict(color='white', size=12),
    width=1000,
    height=900,
    
    # Add range slider for x-axis
    xaxis=dict(
        rangeslider=dict(visible=True),
        type="log",  # Use log scale to better show solar system planets
        gridcolor='rgba(255,255,255,0.1)'
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        dtick=10  # Set tick interval to 10 to prevent overlapping
    ),
    
    # Legend styling
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(0,0,0,0.8)",
        bordercolor="white",
        borderwidth=1
    ),
    
    # Add annotations
    annotations=[
        dict(
            text="Each dot represents one exoplanet<br>⭐ = Solar System planets for reference",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.5, y=-0.15,  # Moved outside graph area below
            xanchor="center", yanchor="top",
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="white",
            borderwidth=1,
            font=dict(size=10, color="white")
        )
    ]
)

# Add horizontal reference lines for score interpretation
fig.add_hline(y=85, line_dash="dash", line_color="green", 
              annotation_text="Highly Habitable", 
              annotation_position="right")
fig.add_hline(y=60, line_dash="dash", line_color="orange", 
              annotation_text="Marginally Habitable", 
              annotation_position="right")

# Show the plot
fig.show()

# Optional: Save as interactive HTML
fig.write_html("exoplanet_habitability_explorer.html")

# Print some statistics
print(f"\n📊 Dataset Statistics:")
print(f"Total planets analyzed: {len(plot_df)}")
print(f"Highly habitable (score ≥ 85): {len(plot_df[plot_df['goldilocks_score'] >= 85])}")
print(f"Marginally habitable (60 ≤ score < 85): {len(plot_df[(plot_df['goldilocks_score'] >= 60) & (plot_df['goldilocks_score'] < 85)])}")
print(f"Unlikely habitable (score < 60): {len(plot_df[plot_df['goldilocks_score'] < 60])}")
print(f"\nClosest potentially habitable planet: {plot_df[plot_df['goldilocks_score'] >= 85]['sy_dist'].min():.2f} parsecs")
