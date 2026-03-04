import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.inspection import PartialDependenceDisplay

st.title("Modeling & Results")

st.write(
    "This section evaluates a Random Forest classifier trained to predict collision "
    "injury severity. The goal is to understand which factors most influence severity "
    "and how well the model distinguishes between different injury levels."
)

# Load model-ready dataset
df = pd.read_csv("data/cleaned_model_ready.csv")

# Split features and target
X = df.drop(columns=["severity_numeric"])
y = df["severity_numeric"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
clf = RandomForestClassifier(class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
st.header("Feature Importance")

st.write(
    "Feature importance shows which variables the Random Forest relied on most when "
    "predicting injury severity. Higher values indicate stronger influence. This helps "
    "identify the key factors contributing to more severe outcomes."
)

importances = clf.feature_importances_
indices = np.argsort(importances)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(X.columns[indices], importances[indices])
ax.set_title("Feature Importance")
st.pyplot(fig)

# -----------------------------
# CONFUSION MATRIX
# -----------------------------
st.header("Confusion Matrix")

y_pred = clf.predict(X_test)

# Force sklearn to use your actual severity labels 1–5
labels = [1, 2, 3, 4, 5]
cm = confusion_matrix(y_test, y_pred, labels=labels)

fig, ax = plt.subplots()
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    ax=ax,
    xticklabels=labels,
    yticklabels=labels
)
ax.set_xlabel("Predicted Severity")
ax.set_ylabel("Actual Severity")
ax.set_title("Confusion Matrix (Severity Levels 1–5)")
st.pyplot(fig)

st.write(
    "The confusion matrix reveals a strong class imbalance: the model predicts "
    "Class 1 (No Injury) correctly most of the time but struggles to identify "
    "more severe injury classes. This occurs because the dataset contains far "
    "more non‑injury collisions than severe ones, causing the model to favor "
    "the majority class even with class weighting."
)

st.write(
    "Note: Scikit‑learn internally reindexes class labels to start at 0, but this "
    "visualization forces the matrix to display the original severity levels (1–5) "
    "for clarity. Class 1 represents 'No Injury' and Class 5 represents a fatal injury."
)

# -----------------------------
# CLASSIFICATION REPORT
# -----------------------------
st.header("Classification Report")

report = classification_report(y_test, y_pred)
st.text(report)

st.write(
    "Precision and recall are high for Class 0 but very low for Classes 1–4. "
    "This confirms that the model performs well on the majority class but has "
    "difficulty distinguishing between higher severity levels. This limitation "
    "is common in imbalanced safety datasets and should be considered when "
    "interpreting model results."
)
# -----------------------------
# PARTIAL DEPENDENCE PLOTS
# -----------------------------
st.header("Partial Dependence Plots")

st.write(
    "Partial dependence plots show how the model's predicted severity changes as "
    "individual features vary. These plots help interpret the model by isolating "
    "the effect of each feature while averaging out all others."
)

features_to_plot = [
    "Age",
    "Airbag Grouped_Airbag Equipped - Not Activated",
    "Seatbelt Grouped_Seatbelt Used",
    "Time Group_Peak Hours"
]

# Create one plot per feature
for feature in features_to_plot:
    fig, ax = plt.subplots(figsize=(6, 4))
    PartialDependenceDisplay.from_estimator(
        clf,
        X_train,
        [feature],   # single feature
        ax=ax,
        target=5
    )
    st.pyplot(fig)