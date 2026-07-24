import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# DISPLAY SETTINGS
# ==========================

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# ==========================
# LOAD DATASET
# ==========================

df = pd.read_csv("IPL_Cleaned_Dataset_1000.csv")

# ==========================
# DATA CLEANING
# ==========================

# Standardize team names
team_mapping = {
    "CSK": "Chennai Super Kings",
    "MI": "Mumbai Indians",
    "RCB": "Royal Challengers Bengaluru",
    "KKR": "Kolkata Knight Riders",
    "SRH": "Sunrisers Hyderabad"
}

df["Team"] = df["Team"].replace(team_mapping)

# Standardize player names
df["Player_Name"] = df["Player_Name"].str.title()

# Remove leading/trailing spaces
df["Team"] = df["Team"].str.strip()
df["Player_Name"] = df["Player_Name"].str.strip()

# Remove duplicate rows
df = df.drop_duplicates()

# Replace invalid Strike Rate values
df.loc[df["Strike_Rate"] < 0, "Strike_Rate"] = pd.NA
df["Strike_Rate"] = df["Strike_Rate"].fillna(df["Strike_Rate"].median())

# ==========================
# FIRST 5 ROWS
# ==========================

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

# ==========================
# DATASET INFO
# ==========================

print("\n========== DATASET INFO ==========")
print(df.info())

# ==========================
# DESCRIPTIVE STATISTICS
# ==========================

print("\n========== DESCRIPTIVE STATISTICS ==========")
print(df.describe(include="all"))

# ==========================
# MISSING VALUES
# ==========================

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# ==========================
# DUPLICATE RECORDS
# ==========================

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

# ==========================
# PLAYERS IN EACH TEAM
# ==========================

print("\n========== PLAYERS IN EACH TEAM ==========")
print(df["Team"].value_counts())

# ==========================
# TOP 10 RUN SCORERS
# ==========================

print("\n========== TOP 10 RUN SCORERS ==========")
print(df.sort_values(by="Runs", ascending=False)[["Player_Name", "Runs"]].head(10))

# ==========================
# CORRELATION MATRIX
# ==========================

numeric_df = df.select_dtypes(include="number")

print("\n========== CORRELATION ==========")
print(numeric_df.corr())

# ==========================
# HISTOGRAM - RUNS
# ==========================

plt.figure(figsize=(8,5))
sns.histplot(df["Runs"], bins=20, kde=True)
plt.title("Distribution of Runs")
plt.xlabel("Runs")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("runs_distribution.png")
plt.close()

# ==========================
# BOXPLOT - RUNS
# ==========================

plt.figure(figsize=(8,5))
sns.boxplot(x=df["Runs"])
plt.title("Runs Boxplot")
plt.xlabel("Runs")
plt.tight_layout()
plt.savefig("runs_boxplot.png")
plt.close()

# ==========================
# BAR CHART - TEAM COUNTS
# ==========================

plt.figure(figsize=(10,5))
df["Team"].value_counts().plot(kind="bar")
plt.title("Players in Each Team")
plt.xlabel("Team")
plt.ylabel("Number of Players")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("team_counts.png")
plt.close()

# ==========================
# HEATMAP
# ==========================

plt.figure(figsize=(10,8))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.close()

# ==========================
# BUSINESS INSIGHTS
# ==========================

print("\n========== BUSINESS INSIGHTS ==========")

# Highest Run Scorer
highest_runs = df.loc[df["Runs"].idxmax()]
print(f"Highest Run Scorer : {highest_runs['Player_Name']} ({highest_runs['Runs']} Runs)")

# Highest Strike Rate
highest_sr = df.loc[df["Strike_Rate"].idxmax()]
print(f"Highest Strike Rate : {highest_sr['Player_Name']} ({highest_sr['Strike_Rate']:.2f})")

# Team with Most Players
team_counts = df["Team"].value_counts()
print(f"Team with Most Players : {team_counts.idxmax()} ({team_counts.max()} Players)")

# Average Runs
print(f"Average Runs : {df['Runs'].mean():.2f}")

# Average Player Price
print(f"Average Player Price : {df['Player_Price_Cr'].mean():.2f} Cr")

# Total Players
print(f"Total Players : {len(df)}")

# Total Teams
print(f"Total Teams : {df['Team'].nunique()}")

# ==========================
# END
# ==========================

print("\nCharts saved successfully!")
print("EDA Completed Successfully!")