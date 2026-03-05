import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

st.title("Modeling & Results")

st.write(
    "This section evaluates a Random Forest classifier trained to predict collision "
    "injury severity. The goal is to understand which factors most influence severity "
    "and how well the model distinguishes between different injury levels. "
    "We also fit a logistic regression model to study interaction effects such as "
    "Age × Seatbelt Use and Age × Airbag Deployment."
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

# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.header("Feature Importance")

st.write(
    "Feature importance shows which variables the Random Forest relied on most when "
    "predicting injury severity. Higher values indicate stronger influence."
)

importances = clf.feature_importances_
indices = np.argsort(importances)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(X.columns[indices], importances[indices])
ax.set_title("Feature Importance")
st.pyplot(fig)

# ============================================================
# CONFUSION MATRIX
# ============================================================

st.header("Confusion Matrix")

y_pred = clf.predict(X_test)

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
    "more severe injury classes."
)

# ============================================================
# CLASSIFICATION REPORT
# ============================================================

st.header("Classification Report")

report = classification_report(y_test, y_pred)
st.text(report)

st.write(
    "Precision and recall are high for Class 1 but very low for Classes 4–5. "
    "This confirms that the model performs well on the majority class but has "
    "difficulty distinguishing between higher severity levels."
)

# ============================================================
# LOGISTIC REGRESSION INTERACTION MODEL
# ============================================================

st.header("Interaction Modeling with Logistic Regression")

st.write(
    "To better understand how specific factors interact to influence severe injury risk, "
    "a logistic regression model was fit using key predictors and their interaction terms. "
    "This allows us to isolate how age interacts with seatbelt use and airbag deployment "
    "to affect the probability of a severe injury."
)

# Prepare data
df_clean = df.copy()
df_encoded = pd.get_dummies(df_clean, drop_first=False)

# Severe injury flag (4–5)
df_clean["severe_injury"] = (df_clean["severity_numeric"] >= 4).astype(int)

# Interaction features
df_clean["no_seatbelt"] = df_encoded["Seatbelt Grouped_No Restraints Used"]

df_clean["airbag_deployed"] = (
    (df_encoded["Airbag Grouped_Airbag Equipped - Not Activated"] == 0) &
    (df_encoded["Airbag Grouped_Not Airbag Equipped"] == 0)
).astype(int)

df_clean["Age_x_NoSeatbelt"] = df_clean["Age"] * df_clean["no_seatbelt"]
df_clean["Age_x_Airbag"] = df_clean["Age"] * df_clean["airbag_deployed"]

# Logistic regression design matrix
X_lr = df_clean[[
    "Age",
    "no_seatbelt",
    "airbag_deployed",
    "Age_x_NoSeatbelt",
    "Age_x_Airbag"
]]

X_lr = sm.add_constant(X_lr).astype(float)
y_lr = df_clean["severe_injury"].astype(int)

logit_model = sm.Logit(y_lr, X_lr)
result = logit_model.fit()

st.subheader("Logistic Regression Summary")
st.text(result.summary())

# ============================================================
# INTERACTION EFFECT: AGE × SEATBELT USE
# ============================================================

st.subheader("Interaction Effect: Age × Seatbelt Use")

ages = np.linspace(16, 90, 100)

df_no = pd.DataFrame({
    "const": 1,
    "Age": ages,
    "no_seatbelt": 1,
    "airbag_deployed": 0,
    "Age_x_NoSeatbelt": ages * 1,
    "Age_x_Airbag": ages * 0
})

df_yes = pd.DataFrame({
    "const": 1,
    "Age": ages,
    "no_seatbelt": 0,
    "airbag_deployed": 0,
    "Age_x_NoSeatbelt": ages * 0,
    "Age_x_Airbag": ages * 0
})

pred_no = result.predict(df_no)
pred_yes = result.predict(df_yes)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ages, pred_yes, label="With Seatbelt")
ax.plot(ages, pred_no, label="Without Seatbelt", linestyle="--")
ax.set_xlabel("Age")
ax.set_ylabel("Predicted Probability of Severe Injury")
ax.set_title("Interaction Effect: Age × Seatbelt Use")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.write(
    "Not wearing a seatbelt increases the probability of a severe injury across all ages, "
    "with the gap widening for older drivers. This interaction suggests that seatbelts "
    "provide increasing protective benefit as age increases."
)

# ============================================================
# INTERACTION EFFECT: AGE × AIRBAG CONDITION
# ============================================================

st.subheader("Interaction Effect: Age × Airbag Condition")

def make_df(airbag_deployed):
    return pd.DataFrame({
        "const": 1,
        "Age": ages,
        "no_seatbelt": 0,
        "airbag_deployed": airbag_deployed,
        "Age_x_NoSeatbelt": 0,
        "Age_x_Airbag": ages * airbag_deployed
    })

df_deployed = make_df(1)
df_not_activated = make_df(0)
df_not_equipped = make_df(0)

pred_deployed = result.predict(df_deployed)
pred_not_activated = result.predict(df_not_activated)
pred_not_equipped = result.predict(df_not_equipped)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ages, pred_deployed, label="Airbag Deployed")
ax.plot(ages, pred_not_activated, label="Airbag Not Activated", linestyle="--")
ax.plot(ages, pred_not_equipped, label="No Airbag Equipped", linestyle=":")
ax.set_xlabel("Age")
ax.set_ylabel("Predicted Probability of Severe Injury")
ax.set_title("Interaction Effect: Age × Airbag Condition")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.write(
    "The model suggests that when an airbag deploys, the predicted probability of severe "
    "injury increases more sharply with age. This does not imply airbags cause harm; "
    "rather, deployment typically occurs in more severe crashes, and older occupants "
    "are more vulnerable to injury."
)
