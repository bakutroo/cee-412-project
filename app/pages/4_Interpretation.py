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
df = pd.read_csv("app/data/cleaned_model_ready.csv")

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

# ----------------------------
# Interactive Tabs
# ----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Feature Importance",
    "Confusion Matrix",
    "Classification Report",
    "Logistic Regression",
    "Interactions"
])

# ============================================================
# TAB 1 — FEATURE IMPORTANCE
# ============================================================
with tab1:
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

    st.write(
    "The feature importance chart shows how much each variable contributed to the "
    "Random Forest model’s ability to predict injury severity. In this model, Age "
    "appears as the most influential predictor, being more than half of the "
    "total importance. This does not mean that age has the strongest linear effect on "
    "injury severity but means that age was the most useful variable for the "
    "Random Forest when splitting the data into purer groups. Random Forests capture "
    "nonlinear patterns and threshold effects, so even if age is not statistically "
    "significant in a logistic regression, it can still provide substantial predictive "
    "value by helping the model identify high‑risk subgroups.\n\n"
    "Other variables like airbag status, time of day, and seatbelt use also "
    "contribute to the model but to a lesser extent. Their lower importance values "
    "indicate that, while they do help the model make accurate predictions, they are "
    "not used as frequently or effectively in the tree‑splitting process as age. For "
    "example, seatbelt non‑use is an expected predictor of severe injury, but "
    "because Random Forests rely on many small splits across many trees, the model may "
    "distribute that information across multiple related variables (e.g., seatbelt "
    "used, no restraints used, ejection status), reducing the importance score of any "
    "single one.\n\n"
    "Overall, the plot highlights that Age provides the most consistent and "
    "informative splits for the Random Forest, while other crash‑related variables "
    "still matter but play more specific  or context‑dependent roles in the model’s "
    "decision‑making."
)

# ============================================================
# TAB 2 — CONFUSION MATRIX
# ============================================================
with tab2:
    st.header("Confusion Matrix")

    y_pred = clf.predict(X_test)

    labels = [1, 2, 3, 4, 5]
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    cm_df = pd.DataFrame(cm, index=labels, columns=labels)

    st.code(cm_df.to_string())

    st.write(
    "The confusion matrix shows that the model performs very well on Class 1 "
    "(No Injury), correctly predicting most of those cases. This happens because "
    "Class 1 is the most common outcome in the dataset, and the model learns "
    "to favor the majority class.\n\n"
    "However, the model struggles significantly with the more severe injury classes. "
    "Classes 2, 3, 4, and 5 are frequently misclassified as lower‑severity outcomes, "
    "often defaulting back to Class 1. This pattern reflects a strong class "
    "imbalance, where the model does not receive enough examples of severe injuries "
    "to learn clear decision boundaries.\n\n"
    "The most severe categories, Classes 4 and 5, are not well predicted. "
    "Their low frequency makes them especially difficult for the model to identify, "
    "and the Random Forest tends to prioritize splits."
    )

# ============================================================
# TAB 3 — CLASSIFICATION REPORT
# ============================================================
with tab3:
    st.header("Classification Report")

    report = classification_report(y_test, y_pred)
    st.code(report)

    st.write(
    "The classification report shows that the model performs well on **Class 1**, "
    "which has the most data. Precision, recall, and f1‑score are all much higher "
    "for this class because the model has many examples to learn from.\n\n"
    "For Classes 2 and 3, the scores are much lower. The model often predicts "
    "these cases as Class 1, which means it struggles to tell the moderate injury "
    "levels apart from the no‑injury class.\n\n"
    "Classes 4 and 5 have extremely low support, so the model struggles to "
    "predict them correctly. With so few examples, it cannot learn their patterns, "
    "leading to very low precision, recall, and f1‑scores.\n\n"
    "Overall, the report shows that the model is good at predicting the majority "
    "class but performs poorly on the more severe injury classes due to class "
    "imbalance and limited training examples."
)
# ============================================================
# TAB 4 — LOGISTIC REGRESSION
# ============================================================
with tab4:
    st.header("Logistic Regression")

    st.write(
        "A logistic regression model was fit to study how age interacts with seatbelt use "
        "and airbag deployment to influence the probability of severe injury."
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
        "Age_x_Airbag",
        "Time Group_Off-Peak",
        "Time Group_Peak Hours",
        "Eject Desc_Totally Ejected",
        "Eject Desc_Partially Ejected"
    ]]

    X_lr = sm.add_constant(X_lr).astype(float)
    y_lr = df_clean["severe_injury"].astype(int)

    logit_model = sm.Logit(y_lr, X_lr)
    result = logit_model.fit()

    st.code(result.summary().as_text())

    st.write(
        "The logistic regression model indicates that seatbelt non-use is the "
        "strongest predictor of severe injury. Airbag deployment is also a "
        "significant positive predictor, reflecting that crashes severe enough "
        "to trigger an airbag are strongly associated with higher injury severity. "
        " Age alone does not significantly affect "
        "injury severity, and it does not significantly impact the effect of "
        "seatbelt use. The interaction between age and airbag deployment is "
        "statistically significant, suggesting that older individuals "
        "experience higher injury severity in crashes severe enough to "
        "trigger airbag deployment."
        )


# ============================================================
# TAB 5 — INTERACTION EFFECTS
# ============================================================
with tab5:
    st.header("Interaction Effects")

    ages = np.linspace(16, 90, 100)

    # ----------------------------
    # Age × Seatbelt Use
    # ----------------------------
    st.subheader("Interaction Effect: Age × Seatbelt Use")

    df_no = pd.DataFrame({
        "const": 1,
        "Age": ages,
        "no_seatbelt": 1,
        "airbag_deployed": 0,
        "Age_x_NoSeatbelt": ages * 1,
        "Age_x_Airbag": ages * 0,
        "Time Group_Off-Peak": 0,
        "Time Group_Peak Hours": 0,
        "Eject Desc_Totally Ejected": 0,
        "Eject Desc_Partially Ejected": 0
    })

    df_yes = pd.DataFrame({
        "const": 1,
        "Age": ages,
        "no_seatbelt": 0,
        "airbag_deployed": 0,
        "Age_x_NoSeatbelt": ages * 0,
        "Age_x_Airbag": ages * 0,
        "Time Group_Off-Peak": 0,
        "Time Group_Peak Hours": 0,
        "Eject Desc_Totally Ejected": 0,
        "Eject Desc_Partially Ejected": 0
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
        "The interaction plot shows that seatbelt use "
        "reduces the probability of severe injury across all ages. Among unbelted drivers, "
        "younger individuals exhibit the highest predicted risk, which gradually declines with age. "
        "However, when a seatbelt is worn, age has basically no effect on severe injury probability, "
        "indicating that seatbelt use eliminates age-related differences in risk."
    )

    # ----------------------------
    # Age × Airbag Condition
    # ----------------------------
    st.subheader("Interaction Effect: Age × Airbag Condition")

    def make_df(airbag_deployed):
        return pd.DataFrame({
            "const": 1,
            "Age": ages,
            "no_seatbelt": 0,
            "airbag_deployed": airbag_deployed,
            "Age_x_NoSeatbelt": 0,
            "Age_x_Airbag": ages * airbag_deployed,
            "Time Group_Off-Peak": 0,
            "Time Group_Peak Hours": 0,
            "Eject Desc_Totally Ejected": 0,
            "Eject Desc_Partially Ejected": 0
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
    "This plot shows how the predicted probability of severe injury changes with age "
    "under different airbag conditions."
    " When the airbag is deployed, the predicted probability of severe injury "
    "increases with age. This happens because airbags usually deploy only in more "
    "serious crashes, and older occupants are more vulnerable to injury.\n\n"
    "When the airbag is not activated, the probability stays low and almost flat "
    "across all ages. These cases usually involve less severe crashes where the "
    "airbag does not need to deploy."
    " As well, when the vehicle has no airbag equipped, the predicted probability is also "
    "low and stable across age, similar to the non‑activated group.\n\n"
    "Overall, the plot shows that higher predicted injury severity is linked to "
    "airbag deployment, not because airbags cause injuries, but because they deploy "
    "in the most serious crashes, especially affecting older individuals."
)