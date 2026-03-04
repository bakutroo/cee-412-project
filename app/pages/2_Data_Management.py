import streamlit as st
from PIL import Image

st.title("Data Management")

st.header("E/R Diagram")
image = Image.open("images/er_diagram.png")
st.image(image)

st.header("Relational Schema")
st.write("""
**Collision(CollisionID, DateTime, Location, Weather, RoadCond)**
- PK: CollisionID

**Person(PersonID, CollisionID, Age, Gender, Role, InjurySeverity)**
- PK: PersonID
- FK: CollisionID → Collision(CollisionID)

**Vehicle(VehicleID, CollisionID, AirbagStatus, SeatbeltUse
         Ejection, VehicleType)**
- PK: VehicleID
- FK: CollisionID → Collision(CollisionID)
""")
