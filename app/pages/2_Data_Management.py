import streamlit as st
from PIL import Image

st.title("Data Management")

st.header("E/R Diagram")
image = Image.open("images/er_diagram.png")
st.image(image)

st.header("Relational Schema")
st.write("""
**Collision(CollisionID, DateTime, Location_X, Location_Y, AddedDate, ReportNumber)**
- PK: CollisionID

**Person(ParticipantRecordID, Age, Gender, ParticipantType, SeatingPosition, InjuryClass, AirbagStatus, Ejection, Restraint)**
- PK: ParticipantRecordID
- FK: CollisionID → Collision(CollisionID)
         
""")

st.header("Assumptions")
st.write("""
- A Collision can involve many Persons; each Person record belongs to exactly one Collision. 
- Person is modeled as a weak entity because the participant record’s identity and existence are defined only within the context of a 
         Collision; the available key in the source is a row identifier for involvement, not a global PersonID.
- Location_X and Location_Y represent the geographic coordinates of the collision site.
""")

# Assumptions for the E/R Diagram:
#   One person can only be involved in one collision, but one collsion can involve multiple people
#   Person is a weak entity set because the key for person
#   is participant record id, which is not unique to one person but exists because of the collsion report
#   so alone, the person is not uniquely identifiable, therefore is a weak entity set
#   the composite key for person is composed of (collisionID, participantrecordID)