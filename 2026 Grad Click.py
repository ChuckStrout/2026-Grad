import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Load the Excel file
DATA_FILENAME = Path(__file__).parent/'data/2026 GSMUD.xlsx'

dfg = pd.read_excel(DATA_FILENAME, sheet_name="Grad Raw Data")
dfg.columns.values[1] = "PROW"
dfg.columns.values[2] = "PSEAT NUMBER"
dfg.columns.values[4] = "ROW"
dfg.columns.values[5] = "SEAT NUMBER"
dfg.columns.values[11] = "PRONOUNCE"
# Display the DataFrame in Streamlit
st.title("🚀 2026 RMHS Grad Clicker")

#venue_options = ("In PAC", "On Turf", "Click","Data")
#venue = "Click"
#venue = st.radio("Select Venue", venue_options,horizontal=True,)
#venue = st.radio("Select Venue", venue_options, horizontal=True)

ADMIN_PASSWORD = "changethepassword"

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

admin_password = st.sidebar.text_input("Admin password", type="password")

if admin_password:
    if admin_password == ADMIN_PASSWORD:
        st.session_state.admin_unlocked = True
    else:
        st.sidebar.error("Incorrect password")

venue_options = ("In PAC", "On Turf")

if st.session_state.admin_unlocked:
    venue_options = venue_options + ("Click", "Data")

venue = st.radio("Select Venue", venue_options, horizontal=True)


if venue == "In PAC":
    background_color = "#CECEC9"  # in PAC
elif venue == "On Turf":
    background_color = "#f36666"  # on Field
else:
    background_color = "#cc2222"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)



dfg["Last Name"] = dfg["Last Name"].fillna("").astype(str).str.strip()
dfg["First Name"] = dfg["First Name"].fillna("").astype(str).str.strip()

dfg["Full Name"] = dfg["Last Name"] + ", " + dfg["First Name"]

def select_student_name():
    name_options = sorted(
        dfg.loc[dfg["Full Name"].str.strip(", ").ne(""), "Full Name"]
        .astype(str)
        .unique()
    )

    return st.selectbox(
        "Select Your Name",
        options=name_options,
        index=None,
        placeholder="Start typing your last name...",
        key="selected_student_name"
    )

# Graduation
if venue == "Data":
    st.dataframe(dfg)
        
if venue == "In PAC":

    selected_name = select_student_name()
    if selected_name is None:
        st.stop()
    
    selected_row = dfg[dfg["Full Name"] == selected_name].iloc[0]
    st.header("Starting in the PAC ")
    
    sectg=selected_row["SECTION"]
    st.text(f"Sit in the {sectg} Section")
    rowg=selected_row["PROW"]
    st.text(f"Sit in Row: {rowg}")
    snumg=selected_row["PSEAT NUMBER"]
    st.text(f"Sit in Seat Number: {snumg}" )

if venue =="On Turf":

    selected_name = select_student_name()
    if selected_name is None:
        st.stop()

    selected_row = dfg[dfg["Full Name"] == selected_name].iloc[0]
    st.header("On The Turf")
   
    side=selected_row["SIDE"]
    st.text(f"You will be On the Side: {side}")
    rowg=selected_row["ROW"]
    st.text(f"You will Sit in the Row: {rowg}" )
    sng=selected_row["SEAT NUMBER"]
    st.text(f"Sit in Seat Number: {sng}")

if venue == "Click":
    if "row_index" not in st.session_state:
        st.session_state.row_index = 0

    


    row = dfg.iloc[st.session_state.row_index]
    side = row["SIDE"]
    rown = row["ROW"]
    first = row["First Name"]
    middle = row["Middle"]
    seat = row["SEAT NUMBER"]

    if pd.isna(middle):
        middle = ""
    last = row["Last Name"]
    pronounce = row["PRONOUNCE"]
    if pronounce == 0 or pd.isna(pronounce):
        pronounce=""
    honor = row["Honor"]
    st.title(f"{first} {middle} {last}")
    st.subheader(pronounce)
    st.title(honor)
    st.text(f"Side: {side}  Row: {rown} Seat {seat}")
    
    col1, col2= st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous"):
            if st.session_state.row_index > 0:
                st.session_state.row_index -= 1

    with col2:
        if st.button("Next ➡️"):
            if st.session_state.row_index < len(dfg) - 1:
                st.session_state.row_index += 1


st.text(f"")
st.text(f"")
st.text(f"")
st.text(f"")
st.text(f"")
st.text(f"")
st.text(f"")
st.text(f"")
st.text("FINAL VERSION")
st.text("v05282612:32")
