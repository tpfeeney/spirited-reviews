import streamlit as st
import pandas as pd
import numpy as np
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

st.set_page_config(
    page_title="Spirited Reviews",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_sidebar_logo()

# ── Spirited Style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
  h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }

  .stApp {
      background: linear-gradient(135deg, #1a0a00 0%, #2d1400 50%, #1a0a00 100%);
      color: #f5e6d3;
  }
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #120600 0%, #1f0c00 100%) !important;
      border-right: 1px solid rgba(200,100,10,0.25);
  }
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stRadio label,
  [data-testid="stSidebar"] .stCheckbox label {
      color: #f0d5b0 !important;
      font-size: 0.95rem !important;
  }
  [data-testid="stSidebar"] .stMarkdown,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span { color: #f0d5b0 !important; }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 { color: #ffd699 !important; }
  label, .stSelectbox label, .stNumberInput label, .stSlider label,
  .stRadio label, .stCheckbox label, .stMultiSelect label {
      color: #f0d5b0 !important;
      font-size: 0.9rem !important;
  }
  p, li, span, div { color: #f5e6d3; }
  .stNumberInput input, .stTextInput input, .stTextArea textarea {
      background: rgba(255,220,160,0.07) !important;
      border: 1px solid rgba(200,100,10,0.35) !important;
      color: #ffd699 !important;
      border-radius: 6px !important;
  }
  .stSelectbox > div > div, .stMultiSelect > div > div {
      background: rgba(255,220,160,0.07) !important;
      border: 1px solid rgba(200,100,10,0.35) !important;
      color: #ffd699 !important;
  }
  .stButton > button {
      background: linear-gradient(90deg, #7a3e00, #c8640a) !important;
      color: #fff8ef !important;
      border: none !important;
      border-radius: 8px !important;
      font-family: 'Playfair Display', serif !important;
      font-size: 1rem !important;
      padding: 9px 28px !important;
      letter-spacing: 0.5px;
      transition: opacity 0.2s;
  }
  .stButton > button:hover { opacity: 0.88 !important; }
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, rgba(200,100,10,0.12), rgba(120,60,0,0.18));
      border: 1px solid rgba(200,100,10,0.3);
      border-radius: 10px;
      padding: 12px 16px;
  }
  [data-testid="stMetricLabel"] { color: #d4956a !important; font-size: 0.8rem !important; }
  [data-testid="stMetricValue"] { color: #ffd699 !important; font-family: 'Playfair Display', serif !important; }
  [data-testid="stDataFrame"] { border: 1px solid rgba(200,100,10,0.2) !important; border-radius: 8px; }
  .streamlit-expanderHeader {
      background: rgba(255,220,160,0.06) !important;
      border: 1px solid rgba(200,100,10,0.2) !important;
      border-radius: 8px !important;
      color: #f5a944 !important;
  }
  .stAlert { border-radius: 8px !important; }
  hr { border-color: rgba(200,100,10,0.2) !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


st.title("Spirited Reviews 🥃")

df = get_data()

# ── Sidebar controls ──────────────────────────────────────────────────────────
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    del st.session_state["df"]
    st.rerun()

theme = st.sidebar.radio("Table theme", ["Dark", "Light"], horizontal=True)

# ── Display table ─────────────────────────────────────────────────────────────
active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]
reviewer_display = {c: c.capitalize() for c in active_reviewers}

base_cols  = ["date", "link", "brand", "name", "avg", "score"]
tail_cols  = ["age", "proof", "price", "type"]
display_cols = base_cols + active_reviewers + tail_cols

display_df = df[[c for c in display_cols if c in df.columns]].copy()
display_df["date"] = display_df["date"].dt.strftime("%d %B %Y")

# Rename to display-friendly headers
rename_map = {
    "date": "Date", "link": "Video Link", "brand": "Brand",
    "name": "Whiskey Name", "avg": "Avg Score", "score": "Verdict",
    "age": "Age", "proof": "Proof", "price": "Price ($)", "type": "Type",
    **reviewer_display
}
display_df.rename(columns=rename_map, inplace=True)

reviewer_display_names = [reviewer_display[c] for c in active_reviewers]

if theme == "Dark":
    odd_color  = "#1a1a1a"
    even_color = "#2a2a2a"
    hover_color = "#3a3020"
else:
    odd_color  = "#ffffff"
    even_color = "#f2efe8"
    hover_color = "#fdf3dc"

display_df["Avg Score"] = pd.to_numeric(display_df["Avg Score"], errors="coerce")
for col in reviewer_display_names + ["Proof"]:
    if col in display_df.columns:
        display_df[col] = pd.to_numeric(display_df[col], errors="coerce")

# Compute median across active reviewer columns
display_df["Median Score"] = display_df[reviewer_display_names].median(axis=1, skipna=True).round(1)

# Insert Median Score right after Avg Score
cols = list(display_df.columns)
avg_idx = cols.index("Avg Score")
cols.insert(avg_idx + 1, cols.pop(cols.index("Median Score")))
display_df = display_df[cols]

# ── Pre-format columns as strings so Streamlit never renders "None" ───────────
# Numeric score columns → "6.5" or "—"
for col in reviewer_display_names + ["Avg Score", "Median Score"]:
    if col in display_df.columns:
        display_df[col] = display_df[col].apply(
            lambda x: f"{x:.1f}" if pd.notna(x) and x is not None else "—"
        )

# Age → "12 yr" or "NAS"
display_df["Age"] = display_df["Age"].apply(
    lambda x: f"{float(x):.0f} yr" if pd.notna(x) and x is not None else "NAS"
)

# Proof → "117.3" or "—"
if "Proof" in display_df.columns:
    display_df["Proof"] = display_df["Proof"].apply(
        lambda x: f"{x:.1f}" if pd.notna(x) and x is not None else "—"
    )

# Price → "$45" or "—"
display_df["Price ($)"] = display_df["Price ($)"].apply(
    lambda x: f"${float(x):.0f}" if pd.notna(x) and x is not None else "—"
)

text_color = "#eeeeee" if theme == "Dark" else "#222222"

def color_rows(row):
    color = odd_color if row.name % 2 == 0 else even_color
    return [f"background-color: {color}; color: {text_color}"] * len(row)

reviewer_fmt = {}

styled = (
    display_df.reset_index(drop=True).style
    .apply(color_rows, axis=1)
)

st.dataframe(
    styled,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Video Link": st.column_config.LinkColumn("Video Link", display_text="▶ Watch"),
        "Date":       st.column_config.TextColumn("Date"),
    }
)

# ── Scoring key ───────────────────────────────────────────────────────────────
with st.expander("📊 Scoring Key"):
    st.image(
        "https://github.com/tpfeeney/spirited-reviews/blob/main/Scoring_Sheet_Final.jpg?raw=true",
        caption="Spirited Reviews Scoring Guide",
        width=600
    )