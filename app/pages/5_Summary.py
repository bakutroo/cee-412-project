import streamlit as st

st.title("Summary & Conclusions")

st.write(
    "The modeling results show that only a few variables meaningfully predict injury "
    "severity, and the findings only partially support the original hypothesis.\n\n"
    "The Random Forest model identified **Age** as the most influential feature. "
    "Although age was not statistically significant in the logistic regression, it "
    "helped the Random Forest create effective nonlinear splits, making it appear as "
    "the top predictor. Other variables such as seatbelt use, airbag status, and time "
    "of day had much smaller importance values.\n\n"
    "The logistic regression model showed that seatbelt non-use is the "
    "strongest and most statistically significant predictor of severe injury. Airbag "
    "deployment was also associated with higher predicted severity, reflecting the "
    "fact that airbags deploy in more serious crashes. The interaction between age and airbag deployment "
    "is statistically significant, suggesting that older individuals experience higher "
    "injury severity in crashes that trigger airbag deployment.\n\n"
    "The interaction plots demonstrated how age interacts with crash conditions. "
    "When airbags deploy, the predicted probability of severe injury increases with "
    "age, showing that older occupants are more vulnerable in high-impact crashes. "
    "Seatbelt use kept predicted severity low across all ages.\n\n"
    "The confusion matrix and classification report revealed that the model "
    "performs well on the majority class (No Injury) but struggles with moderate and "
    "severe injury classes. This is due to strong class imbalance and the very small "
    "number of severe cases in the dataset.\n\n"
    "Overall, the results show that the hypothesis was only partially supported. "
    "Seatbelt non-use is strongly associated with severe injury, but ejection and "
    "time of day did not emerge as important predictors because they are rare or "
    "not directly related to injury severity. Age and crash conditions play a larger "
    "role in shaping injury outcomes."
)
