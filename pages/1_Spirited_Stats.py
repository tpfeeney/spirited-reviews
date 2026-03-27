import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

st.set_page_config(
    page_title="Spirited Stats",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

import streamlit as st

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
  [data-testid="stSidebar"] span {
      color: #f0d5b0 !important;
  }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
      color: #ffd699 !important;
  }
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
  /* Metrics */
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, rgba(200,100,10,0.12), rgba(120,60,0,0.18));
      border: 1px solid rgba(200,100,10,0.3);
      border-radius: 10px;
      padding: 12px 16px;
  }
  [data-testid="stMetricLabel"] { color: #d4956a !important; font-size: 0.8rem !important; }
  [data-testid="stMetricValue"] { color: #ffd699 !important; font-family: 'Playfair Display', serif !important; }
  /* Dataframes */
  [data-testid="stDataFrame"] { border: 1px solid rgba(200,100,10,0.2) !important; border-radius: 8px; }
  /* Expander */
  .streamlit-expanderHeader {
      background: rgba(255,220,160,0.06) !important;
      border: 1px solid rgba(200,100,10,0.2) !important;
      border-radius: 8px !important;
      color: #f5a944 !important;
  }
  /* Info / warning / error boxes */
  .stAlert { border-radius: 8px !important; }
  hr { border-color: rgba(200,100,10,0.2) !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


add_sidebar_logo()

st.title("Spirited Stats")

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]

# ── Sidebar filters ───────────────────────────────────────────────────────────
if 'type' in df.columns and not df['type'].dropna().empty:
    unique_types = sorted(df['type'].dropna().unique())
    type_option = st.sidebar.radio("Restrict to Type:", options=["All Types"] + unique_types, index=0)
else:
    type_option = "All Types"

if type_option != "All Types":
    df = df[df['type'] == type_option]

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

name_options = ["Overall"] + [r.capitalize() for r in active_reviewers]
selected_name = st.sidebar.radio("Select Person", name_options)
selected_key = selected_name.lower()

# ── Metrics ───────────────────────────────────────────────────────────────────
for col in active_reviewers:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['avg'] = pd.to_numeric(df['avg'], errors='coerce')

scores = df['avg'] if selected_key == "overall" else df[selected_key]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reviews", scores.count())
col2.metric("Min Score",     f"{scores.min():.2f}")
col3.metric("Avg Score",     f"{scores.mean():.2f}")
col4.metric("Max Score",     f"{scores.max():.2f}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("", "")
col2.metric("25th Percentile", f"{scores.quantile(0.25):.2f}")
col3.metric("Median",          f"{scores.median():.2f}")
col4.metric("75th Percentile", f"{scores.quantile(0.75):.2f}")

# ── Boxplot ───────────────────────────────────────────────────────────────────
df_melted = df.melt(
    value_vars=active_reviewers,
    var_name='Person', value_name='Score'
)
df_melted['Person'] = df_melted['Person'].str.capitalize()

people = sorted(df_melted['Person'].unique())
palette = sns.color_palette("pastel", n_colors=len(people))
base_palette = dict(zip(people, palette))

if selected_key == "overall":
    palette_dict = base_palette
else:
    palette_dict = {
        p: base_palette[p] if p == selected_name else 'lightgray'
        for p in people
    }


    # ── Dark plot styling to match app theme ──────────────────────────────────
    plt.rcParams.update({
        'figure.facecolor': '#1a0a00',
        'axes.facecolor':   '#2d1400',
        'axes.edgecolor':   '#7a3e00',
        'axes.labelcolor':  '#f5e6d3',
        'xtick.color':      '#f0d5b0',
        'ytick.color':      '#f0d5b0',
        'text.color':       '#f5e6d3',
        'grid.color':       '#3a1800',
        'grid.alpha':       0.4,
    })

fig, ax = plt.subplots(figsize=(max(10, len(people) * 1.5), 5))
fig.patch.set_facecolor('#1a0a00')
ax.set_ylim(0, 10)
sns.boxplot(data=df_melted, x='Person', y='Score', ax=ax, palette=palette_dict)
ax.set_title(f"Score Distribution by Person — {type_option}")
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)