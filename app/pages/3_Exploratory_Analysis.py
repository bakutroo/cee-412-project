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

# ============================================================
# 1. OVERALL SEVERITY PATTERNS
# ============================================================

st.header("Injury Severity Overview")

st.subheader("Injury Severity Distribution")
fig, ax = plt.subplots()
sns.countplot(data=df_eda, x="severity_numeric", ax=ax)
ax.set_xlabel("Severity Level (1 = No Injury, 5 = Fatal Injury)")
ax.set_ylabel("Count")
st.pyplot(fig)

# ============================================================
# 2. AGE-RELATED PATTERNS
# ============================================================

st.header("Age and Injury Severity")

st.subheader("Age Distribution by Injury Severity")
fig, ax = plt.subplots()
sns.boxplot(x="severity_numeric", y="Age", data=df_eda, ax=ax)
ax.set_xlabel("Severity Level")
ax.set_ylabel("Age")
st.pyplot(fig)

st.subheader("Severe vs Non-Severe Injuries by Age")
df_eda["severe_flag"] = df_eda["severity_numeric"].apply(
    lambda x: "Severe (4–5)" if x >= 4 else "Non-Severe (1–3)"
)
fig, ax = plt.subplots()
sns.boxplot(x="severe_flag", y="Age", data=df_eda, ax=ax)
ax.set_xlabel("Injury Category")
ax.set_ylabel("Age")
st.pyplot(fig)

st.subheader("Age Distribution: Severe vs Non-Severe Injuries")
df_eda["severe_injury"] = df_eda["severity_numeric"].apply(lambda x: 1 if x >= 4 else 0)
fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

sns.histplot(
    data=df_eda[df_eda["severe_injury"] == 0],
    x="Age",
    bins=30,
    ax=axes[0]
)
axes[0].set_title("Non-Severe Injuries (Severity 1–3)")
axes[0].set_ylabel("Count")

sns.histplot(
    data=df_eda[df_eda["severe_injury"] == 1],
    x="Age",
    bins=30,
    color="red",
    ax=axes[1]
)
axes[1].set_title("Severe Injuries (Severity 4–5)")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")

st.pyplot(fig)

# ============================================================
# 3. PROTECTIVE FACTORS (SEATBELTS & AIRBAGS)
# ============================================================

st.header("Protective Factors and Severity")

# Convert severity to string for categorical plots
df_eda["severity_numeric"] = df_eda["severity_numeric"].astype(str)

st.subheader("Seatbelt Usage vs Injury Severity")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(
    data=df_eda,
    x="Seatbelt Grouped",
    hue="severity_numeric",
    ax=ax
)
ax.set_xlabel("Seatbelt Usage")
ax.set_ylabel("Count")
st.pyplot(fig)

st.subheader("Airbag Deployment vs Injury Severity")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(
    data=df_eda,
    x="Airbag Grouped",
    hue="severity_numeric",
    ax=ax
)
ax.set_xlabel("Airbag Status")
ax.set_ylabel("Count")
st.pyplot(fig)

# Convert severity back to numeric for heatmap + time averages
df_eda["severity_numeric"] = pd.to_numeric(df_eda["severity_numeric"], errors="coerce")

st.subheader("Interaction: Airbag Deployment and Age Group")
bins = [0, 20, 30, 40, 50, 60, 70, 80, 100]
labels = ['0–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70–79', '80+']
df_eda["Age Group"] = pd.cut(df_eda["Age"], bins=bins, labels=labels, right=False)

pivot_table = df_eda.pivot_table(
    index="Airbag Grouped",
    columns="Age Group",
    values="severity_numeric",
    aggfunc="mean",
    observed=False
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot_table, annot=True, cmap="YlOrRd", fmt=".2f", ax=ax)
ax.set_title("Average Injury Severity by Airbag Type and Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("Airbag Status")
st.pyplot(fig)

# ============================================================
# 4. TIME-RELATED PATTERNS
# ============================================================

st.header("Time of Day and Severity")

# Convert severity to string for categorical plot
df_eda["severity_numeric"] = df_eda["severity_numeric"].astype(str)

st.subheader("Time of Day vs Injury Severity")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(
    data=df_eda,
    x="Time Group",
    hue="severity_numeric",
    ax=ax
)
ax.set_xlabel("Time of Day")
ax.set_ylabel("Count")
st.pyplot(fig)

# Convert back to numeric for averaging
df_eda["severity_numeric"] = pd.to_numeric(df_eda["severity_numeric"], errors="coerce")

# NEW PLOT YOU REQUESTED
st.subheader("Average Injury Severity by Time Group")
fig, ax = plt.subplots(figsize=(8, 5))
df_eda.groupby("Time Group")["severity_numeric"].mean().plot(
    kind="bar",
    ax=ax,
    title="Average Severity by Time Group"
)
ax.set_ylabel("Average Severity")
st.pyplot(fig)

st.subheader("Average Injury Severity by Hour of Day")
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