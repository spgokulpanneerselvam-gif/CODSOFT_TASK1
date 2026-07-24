import pandas as pd

# ==========================
# LOAD DATASET
# ==========================

df = pd.read_csv("IPL_Messy_Dataset_1000.csv")

# ==========================
# FIRST 5 ROWS
# ==========================

print("===== FIRST 5 ROWS =====")
print(df.head())

# ==========================
# DATASET INFO
# ==========================

print("\n===== DATASET INFO =====")
df.info()

# ==========================
# SHAPE
# ==========================

print("\n===== SHAPE =====")
print(df.shape)

# ==========================
# COLUMN NAMES
# ==========================

print("\n===== COLUMN NAMES =====")
print(df.columns)

# ==========================
# DATA TYPES
# ==========================

print("\n===== DATA TYPES =====")
print(df.dtypes)

# ==========================
# MISSING VALUES
# ==========================

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# ==========================
# DUPLICATE ROWS
# ==========================

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

# ==========================
# CLEAN MISSING VALUES
# ==========================

df["Strike_Rate"] = df["Strike_Rate"].fillna(df["Strike_Rate"].mean())
df["Player_Price_Cr"] = df["Player_Price_Cr"].fillna(df["Player_Price_Cr"].mean())

# Optional (recommended)
df["Runs"] = df["Runs"].fillna(df["Runs"].mean())
df["Country"] = df["Country"].fillna("Unknown")

# ==========================
# REMOVE DUPLICATES
# ==========================

df = df.drop_duplicates()

print("\n===== MISSING VALUES AFTER CLEANING =====")
print(df.isnull().sum())

print("\n===== TOTAL DUPLICATE ROWS AFTER CLEANING =====")
print(df.duplicated().sum())

# ==========================
# SAVE CLEANED DATASET
# ==========================

df.to_csv("IPL_Cleaned_Dataset_1000.csv", index=False)

print("\n===== Cleaned Dataset Saved Successfully =====")
