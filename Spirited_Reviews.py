
import streamlit as st
import pandas as pd

st.title("Spirited Reviews")

# --- Load data ---
@st.cache_data
def load_data():
    # Replace with your actual data source
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

df = load_data()

st.dataframe(df, use_container_width=True, hide_index=True, column_order=["date","brand","name","avg","score","randy","norm","zach","justin"])

st.image("Scoring_Sheet_Final.jpg", caption="Scoring Key", width=600)


