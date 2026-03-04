import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Exploratory Analysis")

# Load the cleaned EDA dataset
df_eda = pd.read_csv("data/cleaned_for_eda.csv")

st.write(
    "This page explores key patterns in the cleaned collision dataset, including "
    "severity distribution, age patterns, and relationships with seatbelt use, "
    "airbag deployment, and time of day."
)

# -----------------------------
# Severity Distribution
# -----------------------------
st.subheader("Injury Severity Distribution")

fig, ax = plt.subplots()
sns.countplot(data=df_eda, x="severity_numeric", ax=ax)
ax.set_xlabel("Severity Level (1 = No Injury, 5 = Fatal Injury)")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Age Distribution by Severity
# -----------------------------
st.subheader("Age Distribution by Injury Severity")

fig, ax = plt.subplots()
sns.boxplot(x="severity_numeric", y="Age", data=df_eda, ax=ax)
ax.set_xlabel("Severity Level")
ax.set_ylabel("Age")
st.pyplot(fig)

# -----------------------------
# Severe vs Non-Severe by Age
# -----------------------------
st.subheader("Severe vs Non-Severe Injuries by Age")

df_eda["severe_flag"] = df_eda["severity_numeric"].apply(lambda x: "Severe (4–5)" if x >= 4 else "Non-Severe (1–3)")

fig, ax = plt.subplots()
sns.boxplot(x="severe_flag", y="Age", data=df_eda, ax=ax)
ax.set_xlabel("Injury Category")
ax.set_ylabel("Age")
st.pyplot(fig)

# -----------------------------
# Seatbelt Usage vs Severity
# -----------------------------
st.subheader("Seatbelt Usage vs Injury Severity")

# FIX: convert severity to string for seaborn legend
df_eda["severity_numeric"] = df_eda["severity_numeric"].astype(str)

fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_eda, x="Seatbelt Grouped", hue="severity_numeric", ax=ax)
ax.set_xlabel("Seatbelt Usage")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Airbag Deployment vs Severity
# -----------------------------
st.subheader("Airbag Deployment vs Injury Severity")

fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_eda, x="Airbag Grouped", hue="severity_numeric", ax=ax)
ax.set_xlabel("Airbag Status")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Time of Day vs Severity
# -----------------------------
st.subheader("Time of Day vs Injury Severity")

fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_eda, x="Time Group", hue="severity_numeric", ax=ax)
ax.set_xlabel("Time of Day")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Correlation Heatmap (Numeric Only)
# -----------------------------
st.subheader("Correlation Heatmap (Numeric Features)")

numeric_cols = ["Age", "severity_numeric"]
fig, ax = plt.subplots()
sns.heatmap(df_eda[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# -----------------------------
# Average Severity by Hour of Day
# -----------------------------
st.subheader("Average Injury Severity by Hour of Day")

# Ensure severity is treated as numeric for averaging
df_eda["severity_numeric"] = pd.to_numeric(df_eda["severity_numeric"], errors="coerce")

# Check if Hour column exists
if "Hour" in df_eda.columns:
    hourly_severity = df_eda.groupby("Hour")["severity_numeric"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_severity.index, hourly_severity.values, marker="o")
    ax.set_title("Average Injury Severity by Hour of Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Severity")
    ax.set_xticks(range(0, 24))
    ax.grid(True)

    st.pyplot(fig)

    st.markdown("""
    Severity tends to be **higher during late-night hours**, even though fewer crashes occur then.
    Midday hours show the **lowest average severity**, suggesting that nighttime driving conditions
    (reduced visibility, fatigue, impaired driving) may contribute to more severe outcomes.
    """)
else:
    st.warning("Hour column not found in dataset.")