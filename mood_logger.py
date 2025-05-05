import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px
import json 

# Initialize mood in session state
if "mood" not in st.session_state:
    st.session_state["mood"] = None

st.markdown("<h1 style='font-size: 48px;'>How are things feeling?</h1>", unsafe_allow_html=True)

# Emoji buttons with persistent selection
moods = {
    "😊": "happy",
    "😠": "angry",
    "😕": "confused",
    "🎉": "celebratory"
}

cols = st.columns(len(moods))
for i, (emoji, mood_name) in enumerate(moods.items()):
    if cols[i].button(emoji):
        st.session_state["mood"] = mood_name

# Show which mood is selected
if st.session_state["mood"]:
    st.markdown(f"**Selected mood:** {st.session_state['mood']}")

st.markdown("""
    <style>
    button[kind="secondary"] {
        font-size: 40px !important;
        height: 80px !important;
        width: 80px !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h2 style='font-size: 32px;'>Optional note:</h2>", unsafe_allow_html=True)
note = st.text_area("Optional note:")

def append_to_sheet(mood, note):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Load creds from secrets
    creds_dict = json.loads(st.secrets["creds"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    # creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Open sheet by name
    sheet = client.open("Mood Logger").sheet1

    # Append row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])

if st.button("Submit") and st.session_state["mood"]:
    append_to_sheet(st.session_state["mood"], note)
    st.success("Mood logged successfully!")

# Helper to fetch sheet as DataFrame
def get_today_mood_counts():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Load creds from secrets
    creds_dict = json.loads(st.secrets["creds"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    # creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mood Logger").sheet1
    data = sheet.get_all_records()
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    today = pd.Timestamp.now().normalize()
    df_today = df[df['timestamp'].dt.normalize() == today]
    
    mood_counts = df_today['mood'].value_counts().reset_index()
    mood_counts.columns = ['mood', 'count']
    return mood_counts

# Show the bar chart
if st.button("Show Mood Chart"):
    mood_counts = get_today_mood_counts()
    if not mood_counts.empty:
        fig = px.bar(mood_counts, x='mood', y='count', color='mood', title="Today's Mood Summary")
        st.plotly_chart(fig)
    else:
        st.info("No moods logged yet today.")
