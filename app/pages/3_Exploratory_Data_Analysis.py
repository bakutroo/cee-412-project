import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Exploratory Data Analysis")

# Load the cleaned EDA dataset
df_eda = pd.read_csv("app/data/cleaned_for_eda.csv")

# ----------------------------
# Sidebar Filters (EDA Only)
# ----------------------------
st.sidebar.header("Filter EDA Data")

# Age filter
min_age = int(df_eda["Age"].min())
max_age = int(df_eda["Age"].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# Seatbelt filter
seatbelt_options = df_eda["Seatbelt Grouped"].unique().tolist()
seatbelt_filter = st.sidebar.multiselect(
    "Seatbelt Usage",
    options=seatbelt_options,
    default=seatbelt_options
)

# Airbag filter
airbag_options = df_eda["Airbag Grouped"].unique().tolist()
airbag_filter = st.sidebar.multiselect(
    "Airbag Status",
    options=airbag_options,
    default=airbag_options
)

# Time of day filter
time_options = df_eda["Time Group"].unique().tolist()
time_filter = st.sidebar.multiselect(
    "Time of Day",
    options=time_options,
    default=time_options
)

# Severity filter
severity_options = sorted(df_eda["severity_numeric"].unique().tolist())
severity_filter = st.sidebar.multiselect(
    "Severity Levels",
    options=severity_options,
    default=severity_options
)

# Reset button
if st.sidebar.button("Reset Filters"):
    age_range = (min_age, max_age)
    seatbelt_filter = seatbelt_options
    airbag_filter = airbag_options
    time_filter = time_options
    severity_filter = severity_options

# Apply filters to df_eda
df_eda = df_eda[
    (df_eda["Age"].between(age_range[0], age_range[1])) &
    (df_eda["Seatbelt Grouped"].isin(seatbelt_filter)) &
    (df_eda["Airbag Grouped"].isin(airbag_filter)) &
    (df_eda["Time Group"].isin(time_filter)) &
    (df_eda["severity_numeric"].isin(severity_filter))
]

st.write(
    "This page explores key patterns in the cleaned collision dataset, including "
    "severity distribution, age patterns, and relationships with seatbelt use, "
    "airbag deployment, and time of day. "
    "Use the filters in the sidebar to interactively explore how these patterns "
    "change across different age groups, restraint usage, airbag status, time-of-day "
    "categories, and severity levels."
)
# ----------------------------
# Interactive Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Severity Patterns",
    "Age Patterns",
    "Protective Factors",
    "Time Patterns"
])

# ============================================================
# TAB 1 — SEVERITY PATTERNS
# ============================================================
with tab1:
    st.header("Injury Severity Overview")

    st.subheader("Injury Severity Distribution")
    fig, ax = plt.subplots()

    sns.countplot(data=df_eda, x="severity_numeric", ax=ax)

    # Add count labels on bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{height}",
            (p.get_x() + p.get_width() / 2, height),
            ha="center",
            va="bottom",
            fontsize=10
        )

    ax.set_xlabel("Severity Level (1 = No Injury, 5 = Fatal Injury)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# ============================================================
# TAB 2 — AGE PATTERNS
# ============================================================
with tab2:
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
# TAB 3 — PROTECTIVE FACTORS
# ============================================================
with tab3:
    st.header("Protective Factors and Severity")

    # Convert severity to string for categorical plots
    df_eda["severity_numeric"] = df_eda["severity_numeric"].astype(str)

    # Explicit legend order
    severity_order = ["1.0", "2.0", "3.0", "4.0", "5.0"]

    st.subheader("Seatbelt Usage vs Injury Severity")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=df_eda,
        x="Seatbelt Grouped",
        hue="severity_numeric",
        hue_order=severity_order,
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
        hue_order=severity_order,
        ax=ax
    )
    ax.set_xlabel("Airbag Status")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Convert back to numeric for later analysis
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

    # Heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_table, annot=True, cmap="YlOrRd", fmt=".2f", ax=ax)
    ax.set_title("Average Injury Severity by Airbag Type and Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Airbag Status")
    st.pyplot(fig)

    # Table version
    st.subheader("Numeric Table View (If Numbers Do Not Load on Heatmap)")
    st.dataframe(pivot_table.style.format("{:.2f}"))

# ============================================================
# TAB 4 — TIME PATTERNS
# ============================================================
with tab4:
    st.header("Time of Day and Severity")

    # Convert severity to string for categorical plot
    df_eda["severity_numeric"] = df_eda["severity_numeric"].astype(str)

    # Explicit legend order
    severity_order = ["1.0", "2.0", "3.0", "4.0", "5.0"]

    st.subheader("Time of Day vs Injury Severity")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=df_eda,
        x="Time Group",
        hue="severity_numeric",
        hue_order=severity_order,
        ax=ax
    )
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Convert back to numeric for averaging
    df_eda["severity_numeric"] = pd.to_numeric(df_eda["severity_numeric"], errors="coerce")

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
        Severity tends to be higher during late-night hours, even though fewer crashes occur then.
        Midday hours show the lowest average severity, suggesting that nighttime driving conditions
        (reduced visibility, fatigue, impaired driving) may contribute to more severe outcomes.
        """)
    else:
        st.warning("Hour column not found in dataset.")