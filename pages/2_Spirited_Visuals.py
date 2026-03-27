import streamlit as st
import pandas as pd
import plotly.express as px
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

st.set_page_config(
    page_title="Spirited Visuals",
    page_icon="📈",
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

st.title("Spirited Visualizations")

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]

# ── Data prep ─────────────────────────────────────────────────────────────────
page_df = df.copy()
page_df['age_new'] = pd.to_numeric(page_df['age'], errors='coerce')
page_df['avg']     = pd.to_numeric(page_df['avg'],   errors='coerce')
page_df['proof']   = pd.to_numeric(page_df['proof'], errors='coerce')
page_df['price']   = pd.to_numeric(page_df['price'], errors='coerce')
for c in active_reviewers:
    page_df[c] = pd.to_numeric(page_df[c], errors='coerce')

bins   = [79, 89, 94, 99, 104, 109, 114, 119, 129, 139, 149, float('inf')]
labels = ["80-89","90-94","95-99","100-104","105-109",
          "110-114","115-119","120-129","130-139","140-149",">=150"]
page_df['proof_cat'] = pd.cut(page_df['proof'], bins=bins, labels=labels, right=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
chart_type = st.sidebar.radio(
    "Select chart type:",
    ["Proof Breakdown", "Type Breakdown", "Price v Review",
     "Proof v Review", "Age v Review", "Choose your own adventure"]
)

# ── Charts ────────────────────────────────────────────────────────────────────
if chart_type == "Proof Breakdown":
    proof_df = page_df['proof_cat'].value_counts().sort_index().reset_index()
    proof_df.columns = ['Proof Category', 'Count']
    fig = px.bar(proof_df, x='Proof Category', y='Count',
                 title="Number of Observations per Proof Category",
                 text='Count', color='Proof Category')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, showlegend=False,
                      margin=dict(t=60, b=80), height=500)
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Type Breakdown":
    type_counts = page_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.pie(type_counts, names='type', values='count',
                 title="Distribution of Whiskey Types")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Price v Review":
    fig = px.scatter(page_df, x="price", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "price": "Price ($)"},
                     hover_name="name")
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Proof v Review":
    fig = px.scatter(page_df, x="proof", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "proof": "Proof"},
                     hover_name="name")
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Age v Review":
    age_df = page_df[page_df['age_new'].notna()]
    fig = px.scatter(age_df, x="age_new", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "age_new": "Age"},
                     hover_name="name")
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Choose your own adventure":
    st.sidebar.markdown("### Select X and Y axes")

    all_options = {
        "avg":     "Overall Average",
        "age_new": "Age",
        "price":   "Price ($)",
        "proof":   "Proof",
        **{c: f"{c.capitalize()} Score" for c in active_reviewers},
    }
    allowed_keys = list(all_options.keys())

    x_col_key = st.sidebar.selectbox(
        "X-axis:", options=allowed_keys,
        index=allowed_keys.index("price"),
        format_func=lambda x: all_options[x]
    )
    y_options = [k for k in allowed_keys if k != x_col_key]
    y_col_key = st.sidebar.selectbox(
        "Y-axis:", options=y_options,
        index=y_options.index("avg") if "avg" in y_options else 0,
        format_func=lambda x: all_options[x]
    )
    trendline_option = st.sidebar.radio(
        "Add Trendline", options=["None", "OLS", "LOWESS"], index=1
    )
    trendline_map = {"None": None, "OLS": "ols", "LOWESS": "lowess"}

    fig = px.scatter(
        page_df, x=x_col_key, y=y_col_key,
        trendline=trendline_map[trendline_option],
        labels={x_col_key: all_options[x_col_key], y_col_key: all_options[y_col_key]},
        title=f"{all_options[y_col_key]} vs {all_options[x_col_key]}",
        hover_name="name"
    )
    fig.update_layout(
        paper_bgcolor='#1a0a00',
        plot_bgcolor='#2d1400',
        font=dict(color='#f5e6d3', family='Source Sans 3'),
        title_font=dict(color='#ffd699', family='Playfair Display'),
        xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0'),
        legend=dict(bgcolor='rgba(45,20,0,0.8)', bordercolor='#7a3e00', borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)