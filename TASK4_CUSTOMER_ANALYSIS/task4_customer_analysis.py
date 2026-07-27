# ===========================
# CUSTOMER DATA ANALYSIS
# ===========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("Mall_Customers.csv")

print("First 5 Rows")
print(df.head())

print("\nDataset Info")
print(df.info())

print("\nSummary Statistics")
print(df.describe())

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------
# Customer Segmentation by Age
# ----------------------------

def age_group(age):
    if age <= 25:
        return "Young"
    elif age <= 40:
        return "Adult"
    else:
        return "Senior"

df["Age_Group"] = df["Age"].apply(age_group)

print("\nCustomers by Age Group")
print(df["Age_Group"].value_counts())

# ----------------------------
# High Value Customers
# ----------------------------

high_value = df[df["Spending Score (1-100)"] >= 80]

print("\nHigh Value Customers")
print(high_value)

# ----------------------------
# Average Spending
# ----------------------------

print("\nAverage Spending by Gender")
print(df.groupby("Gender")["Spending Score (1-100)"].mean())

print("\nAverage Income by Gender")
print(df.groupby("Gender")["Annual Income (k$)"].mean())

# ----------------------------
# K-Means Customer Segmentation
# ----------------------------

X = df[['Annual Income (k$)',
        'Spending Score (1-100)']]

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df['Cluster'] = kmeans.fit_predict(X)

print(df.head())

# ----------------------------
# Create Images Folder
# ----------------------------

import os

os.makedirs("images", exist_ok=True)

# ----------------------------
# Age Distribution
# ----------------------------

plt.figure(figsize=(8,5))

sns.histplot(df["Age"], bins=15)

plt.title("Age Distribution")

plt.savefig("images/age_distribution.png")

plt.close()

# ----------------------------
# Income Distribution
# ----------------------------

plt.figure(figsize=(8,5))

sns.histplot(df["Annual Income (k$)"], bins=15)

plt.title("Annual Income Distribution")

plt.savefig("images/income_distribution.png")

plt.close()

# ----------------------------
# Spending Score
# ----------------------------

plt.figure(figsize=(8,5))

sns.histplot(df["Spending Score (1-100)"], bins=15)

plt.title("Spending Score Distribution")

plt.savefig("images/spending_score.png")

plt.close()

# ----------------------------
# Age vs Spending
# ----------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x="Age",
    y="Spending Score (1-100)",
    hue="Gender",
    data=df
)

plt.title("Age vs Spending Score")

plt.savefig("images/age_vs_spending.png")

plt.close()

# ----------------------------
# Customer Segments
# ----------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    hue="Cluster",
    palette="Set2",
    data=df
)

plt.title("Customer Segments")

plt.savefig("images/customer_segments.png")

plt.close()

print("\nAnalysis Completed Successfully!")

print("\nImages Saved in images folder")