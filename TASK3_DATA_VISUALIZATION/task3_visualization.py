import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("IPL_Cleaned_Dataset_1000.csv")
# ==========================
# INSIGHTS
# ==========================

print("\n========== VISUALIZATION INSIGHTS ==========")

# Team with the most players
team_counts = df["Team"].value_counts()
print(f"1. Team with the most players: {team_counts.idxmax()} ({team_counts.max()} players)")

# Highest run scorer
highest_runs = df.loc[df["Runs"].idxmax()]
print(f"2. Highest Run Scorer: {highest_runs['Player_Name']} ({highest_runs['Runs']} runs)")

# Highest strike rate
highest_sr = df.loc[df["Strike_Rate"].idxmax()]
print(f"3. Highest Strike Rate: {highest_sr['Player_Name']} ({highest_sr['Strike_Rate']:.2f})")

# Average runs
print(f"4. Average Runs: {df['Runs'].mean():.2f}")

# Average player price
print(f"5. Average Player Price: {df['Player_Price_Cr'].mean():.2f} Cr")

# Correlation insight
correlation = df["Runs"].corr(df["Strike_Rate"])
print(f"6. Correlation between Runs and Strike Rate: {correlation:.2f}")

print("\nCharts created successfully!")
print("Task 3 Completed Successfully!")