
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import numpy as np

st.title("Spirited Reviews")

def score_label(avg):
    if 0 < avg < 1:
        return "tainted, WTF?!"
    elif 1 <= avg < 2:
        return "Dumpster Fire Adjacent"
    elif 2 <= avg < 3:
        return "Tastes Like Regret"
    elif 3 <= avg < 4:
        return "Last call material"
    elif 4 <= avg < 5:
        return "Questionable Choices"
    elif 5 <= avg < 6:
        return "Has Potential..."
    elif 6 <= avg < 7:
        return "Weeknight Winner"
    elif 7 <= avg < 8:
        return "Shelf-Worthy"
    elif 8 <= avg < 9:
        return "Hello There"
    elif 9 <= avg < 10:
        return "Legen...Wait For It..Dary!"
    elif avg >= 10:
        return "Flawless Victory"
    else:
        return np.nan
        
def add_sidebar_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://github.com/tpfeeney/spirited-reviews/blob/main/srlogo.png?raw=true');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                padding-top: 180px;
                background-size: 150px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_sidebar_logo()


@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    
    # Parse dates and filter
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  
    today = pd.Timestamp.today().normalize()
    df = df[df['date'] <= today - pd.Timedelta(days=2)]
    
    #relabel score
    df['score'] = df['avg'].apply(score_label)

    return df

df=load_data()

# --- Load into session state ---
if "df" not in st.session_state:
    st.session_state.df = load_data()

# --- Display using st.data_editor with link rendering ---
st.data_editor(
    st.session_state.df,
    column_order=[
       "date", "link", "brand", "name", "avg", "score", "randy", "norm", "zach", "justin",
        "age", "proof", "price", "type"  # <--- use raw 'link' column
    ],
    column_config={
        "date": st.column_config.DateColumn("Date", format="DD MMMM YYYY"),
        "link": st.column_config.LinkColumn("Video Link", display_text="Open Review"),
        "brand": st.column_config.TextColumn("Brand"),
        "name": st.column_config.TextColumn("Whiskey Name"),
        "avg": st.column_config.NumberColumn("Average Score"),
        "score": st.column_config.TextColumn("Verdict"),
        "randy": st.column_config.NumberColumn("Randy"),
        "norm": st.column_config.NumberColumn("Norm"),
        "zach": st.column_config.NumberColumn("Zach"),
        "justin": st.column_config.NumberColumn("Justin"),
        "age": st.column_config.NumberColumn("Age"),
        "proof": st.column_config.NumberColumn("Proof"),
        "price": st.column_config.NumberColumn("Price ($)"),
        "type": st.column_config.TextColumn("Style"),
    },
    hide_index=True,
    use_container_width=True
)

st.image("Scoring_Sheet_Final.jpg", caption="Scoring Key", width=600)
