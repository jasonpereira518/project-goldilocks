import pandas as pd
import numpy as np


df = pd.read_csv("cdcdata.csv")

columns = ['pl_name', 'pl_orbsmax', 'pl_orbper', 'st_teff', 'st_rad', 'st_mass', 'pl_rade']
df = df[columns].dropna()

numeric_cols = ['pl_orbsmax', 'pl_orbper', 'st_teff', 'st_rad', 'st_mass', 'pl_rade']


z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())


outlier_mask = (z_scores > 3).any(axis=1)
outliers = df[outlier_mask]


unique_outliers = outliers.drop_duplicates(subset=['pl_name'])


unique_outliers[['pl_name']].to_csv("rogue_planets.csv", index=False)

print("\nUnique Outlier Planets:\n")
print(unique_outliers[['pl_name']])
