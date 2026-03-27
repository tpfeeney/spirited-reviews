import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

st.set_page_config(
    page_title="Distillery Ranks",
    page_icon="🏆",
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

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

if 'type' not in df.columns:
    st.error("'type' column not found in the dataframe.")
    st.stop()

# ── Legacy distillery list ────────────────────────────────────────────────────
legacy_brands = [
    "Jack Daniel's", "Heaven Hill", "Jim Beam", "Bardstown", "Maker's Mark",
    "Wild Turkey", "Buffalo Trace", "Four Roses", "MGP",
    "Old Forester", "Willett"
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("Filters")

distillery_option = st.sidebar.radio("Select Distillery Type:", ("All", "Legacy Distillery"))

unique_types = sorted(df['type'].dropna().unique())
type_option = st.sidebar.radio("Restrict to Type:", options=["All Types"] + list(unique_types), index=0)

reviewers = [c for c in REVIEWER_COLS if c in df.columns]
selected_reviewers = []

st.sidebar.markdown("### Select Reviewers (including Overall)")
if st.sidebar.checkbox("Overall", value=True):
    selected_reviewers.append('avg')
for r in reviewers:
    if st.sidebar.checkbox(r.capitalize(), value=True):
        selected_reviewers.append(r)

# ── Filter ────────────────────────────────────────────────────────────────────
df_filtered = df.copy()
if distillery_option == "Legacy Distillery":
    df_filtered = df_filtered[df_filtered['brand'].isin(legacy_brands)]
if type_option != "All Types":
    df_filtered = df_filtered[df_filtered['type'] == type_option]

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.sidebar.markdown("---")
theme = st.sidebar.radio("Table theme", ["Dark", "Light"], horizontal=True)

# ── Average scores table ──────────────────────────────────────────────────────
st.header("Average Scores by Brand")

grouped = df_filtered.groupby('brand')[selected_reviewers].mean().reset_index()
review_counts = df_filtered.groupby('brand').size().reset_index(name='# of Reviews')
grouped = pd.merge(grouped, review_counts, on='brand', how='left')

rename_dict = {r: ("Overall Avg" if r == 'avg' else f"{r.capitalize()} Avg") for r in selected_reviewers}
grouped.rename(columns=rename_dict, inplace=True)

sort_col = "Overall Avg" if "Overall Avg" in grouped.columns else grouped.columns[1]
grouped = grouped.round(2).sort_values(by=sort_col, ascending=False).reset_index(drop=True)

if theme == "Dark":
    odd_color  = "#1a1a1a"
    even_color = "#2a2a2a"
    text_color = "#eeeeee"
else:
    odd_color  = "#ffffff"
    even_color = "#f2efe8"
    text_color = "#222222"

def color_rows(row):
    color = odd_color if row.name % 2 == 0 else even_color
    return [f"background-color: {color}; color: {text_color}"] * len(row)

avg_cols = [col for col in grouped.columns if 'Avg' in col]
styled = (
    grouped.style
    .apply(color_rows, axis=1)
    .format({col: "{:.2f}" for col in avg_cols})
)

st.dataframe(styled, use_container_width=True, hide_index=True)

# ── Boxplot — dynamic height based on brand count ─────────────────────────────
if selected_reviewers:
    st.header("Score Distribution by Brand")

    df_melted = df_filtered[['brand'] + selected_reviewers].melt(
        id_vars='brand', var_name='Reviewer', value_name='Score'
    )
    df_melted['Reviewer'] = df_melted['Reviewer'].apply(
        lambda x: "Overall" if x == 'avg' else x.capitalize()
    )

    n_brands = df_filtered['brand'].nunique()
    # Scale height with brand count so labels don't get squished
    fig_height = max(4, min(n_brands * 0.6, 16))


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

    fig, ax = plt.subplots(figsize=(max(8, n_brands * 0.8), fig_height))
    fig.patch.set_facecolor('#1a0a00')

    if set(df_melted['Reviewer']) == {"Overall"}:
        sns.boxplot(data=df_melted, x='brand', y='Score', color='skyblue', ax=ax)
    else:
        sns.boxplot(data=df_melted, x='brand', y='Score', hue='Reviewer', ax=ax, palette='pastel')

    title_suffix = f" — {type_option}" if type_option != "All Types" else ""
    ax.set_title(f"Boxplot of Scores by Brand{title_suffix}")
    ax.set_xlabel("Brand")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 10)
    ax.tick_params(axis='x', rotation=45)
    if len(df_melted['Reviewer'].unique()) > 1:
        ax.legend(title="Reviewer", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Please select at least one reviewer.")