
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Spirited Reviews")

@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    
    # Parse dates and filter
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    today = pd.Timestamp.today().normalize()
    df = df[df['date'] <= today - pd.Timedelta(days=3)]

    # Format date as "07 July 2025"
    df['date'] = df['date'].dt.strftime('%d %B %Y')

    return df

# --- Load into session state ---
if "df" not in st.session_state:
    st.session_state.df = load_data()

# --- Display using st.data_editor with link rendering ---
st.data_editor(
    st.session_state.df,
    column_order=[
        "date", "brand", "name", "avg", "score", "randy", "norm", "zach", "justin",
        "age", "proof", "price", "type", "score", "link"  # <--- use raw 'link' column
    ],
    column_config={
        "link": st.column_config.LinkColumn(
            "Review Link",  # Column title
            display_text="Open Review"  # Text to display instead of raw URL
        )
    },
    hide_index=True,
    use_container_width=True
)

st.image("Scoring_Sheet_Final.jpg", caption="Scoring Key", width=600)
