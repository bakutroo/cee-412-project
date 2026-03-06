import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================================
# WE'LL NEED TO MOVE THE FOLLOWING CODE INTO THE PAGE WHERE WE WOULD ACTUALLY BE DISPLAYING THE DATA, 
# OTHERWISE THIS ENTIRE PROCESS WILL RUN BEFORE THE INTRO EVEN POPS UP, OR WE MOVE IT TO AFTER THE INTRO CODE. 
# ----------------------------
# Page config
# ----------------------------
#st.set_page_config(
#    page_title="Traffic Flow Explorer",
#    page_icon="🚦",
#    layout="wide",
#)

#st.title("🚦 Traffic Flow Explorer")
#st.caption("Visualize traffic volume and perform basic exploratory analysis (EDA) with Streamlit.")

# ----------------------------
# Data loading
# ----------------------------
#DEFAULT_PATH = "cleaned_for_eda.csv"  

#@st.cache_data
#def load_data_from_path(path):
 #   df = pd.read_csv(path)
 #   return _prepare_data(df)

#@st.cache_data
#def _prepare_data(df):
    # Made a copy of the dataframe taken from the CSV
   # out = df.copy()

    # Using pandas here to take the data based on the column name
    #  For yalls you'll want to put this, but instead of
    # "DateTime" and "Junction" and "Vehicles" you'll just put
    # the columns you actually want to use here and it should (?)
    # be able to just use that data

    # pd.to_datetime puts this information (in the .csv file) to a specific breakdown
    # through which you can then access specific parts (see below)

    # so for these [] we'll replace them with the columns from the data we are interested in analyzing
    # use to_numeric for all of them, unless we are looking at hours of day (possible)
  #  out["DateTime"] = pd.to_datetime(out["DateTime"], errors="coerce")
   # out["Junction"] = pd.to_numeric(out["Junction"], errors="coerce").astype("Int64")
   # out["Vehicles"] = pd.to_numeric(out["Vehicles"], errors="coerce")

    # This is basic clean up, he's dropping data, rows, and/or columns that are NaN
    #  (Not a Number), or non uniform (could cause many errors)
    # so he's just listing the 'subsets' aka columns he wants this function done on
  #  out = out.dropna(subset=["DateTime", "Junction", "Vehicles"]).copy()
    # 
   # out["Junction"] = out["Junction"].astype(int)

    # Feature engineering for EDA

    # He's now creating another column (?) based on the information he got from breaking down the "DateTime" column above
    # will only need to do this for columns that have multiple types of information that we want to extract. 
    # shouldn't need to do this for any 'to_numeric' ones. 

 #   out["Date"] = out["DateTime"].dt.date
 #   out["Hour"] = out["DateTime"].dt.hour
 #   out["DayOfWeek"] = out["DateTime"].dt.dayofweek  # Monday=0
 #   out["DayName"] = out["DateTime"].dt.day_name()
 #   out["Month"] = out["DateTime"].dt.to_period("M").astype(str)
 #   out["Year"] = out["DateTime"].dt.year

 #   return out.sort_values("DateTime").reset_index(drop=True)

# Optional uploader
#uploaded = st.sidebar.file_uploader("Upload a CSV (optional)", type=["csv"])
#st.sidebar.markdown("If no file is uploaded, the app will try to read `traffic.csv` from the current folder.")

# below, this has already been changed to match our project, shouldn't need any updating
#try:
#   data = load_data_from_path(DEFAULT_PATH)
#    source_name = DEFAULT_PATH
#except Exception as e:
#    st.error(f"Failed to load data: {e}")
#    st.stop()

# he suggested that we work only on data visualization and analysis first, and then do filters
# IF WE HAVE TIME, it wouldn't add enough extra to our analysis unless we have extra time for it. 
# if we do use filters, likely they would have to do with sorting age groups and being able to select one or many of those groups at a time.
# also if we make four agre groups, similar to his four junctions, it would be the simplest to adapt his code for our purposes. 


#st.sidebar.header("Filters")

#all_junctions = sorted(data["Junction"].unique().tolist())
# Visualization of data options while also getting the actual junctions that will be used in the 
# 
#selected_junctions = st.sidebar.multiselect(
 #   "Select junction(s)",
  #  options=all_junctions,
  #  default=all_junctions,
#)

#if not selected_junctions:
#    st.warning("Please select at least one junction.")
#    st.stop()

st.title("CEE 412 Project: Analyzing How Collision and Occupant Attributes Influence Injury Severity – SDOT Collisions")
st.write("Created by Hannah Bacon, Audrey Nielsen, Joy Wang, Melissa Williams")
st.write("Use the sidebar to navigate through the project pages.")
