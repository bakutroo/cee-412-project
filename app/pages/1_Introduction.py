import streamlit as st

st.title("Introduction")

st.markdown("""
### Project Objectives

The purpose of this project is to examine how various participant- and crash-related 
attributes are associated with the severity of injuries sustained in vehicle collisions. 
Injury severity in the dataset is recorded using categories such as *no injury, possible injury, 
non-serious injury, serious injury, died at hospital, dead on arrival,* and *dead at scene*. 
For analysis, these categories were mapped to a numerical scale ranging from **1 (No Injury)** 
to **5 (Fatal Injury)**.

The dataset includes demographic factors (such as age), behavioral factors (seatbelt use, 
distraction indicators), and crash-specific conditions (airbag deployment, ejection status, 
and time of day). Text-based categorical variables were cleaned and consolidated into grouped 
categories (e.g., “Airbag Equipped – Not Activated,” “Seatbelt Used,” “Ejected”) and then 
encoded numerically for modeling.

Using this cleaned dataset, the project develops a predictive model to identify which factors 
are most strongly associated with severe or fatal injuries. The goal is not only to predict 
severity but also to understand which attributes contribute most to high-risk outcomes.

### Hypothesis

Participant-specific factors, such as younger age, lack of seatbelt use, presence of distractions, 
and especially ejection from the vehicle, are expected to be positively associated with higher 
injury severity. Among these, **ejection from the vehicle is hypothesized to have the strongest 
relationship with severe or fatal injury outcomes**.
""")
