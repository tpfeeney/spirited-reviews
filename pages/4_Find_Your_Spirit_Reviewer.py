import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import add_sidebar_logo, get_data, score_label, REVIEWER_COLS

st.set_page_config(
    page_title="Find Your Reviewer",
    page_icon="🎯",
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


st.title("Find your Spirit Reviewer")
st.info(
    "Select whiskeys by checking the boxes, rate them yourself using the sliders, "
    "then see whose palate matches yours most closely."
)

add_sidebar_logo()

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]

# ── Editable table with select checkboxes ─────────────────────────────────────
display_df = df.copy()
if "select" not in display_df.columns:
    display_df["select"] = False

# ── Style the table to match main page ────────────────────────────────────────
styled_df = display_df.copy()

# Format columns for display
for c in active_reviewers + ['avg']:
    if c in styled_df.columns:
        styled_df[c] = pd.to_numeric(styled_df[c], errors='coerce')

if 'proof' in styled_df.columns:
    styled_df['proof'] = pd.to_numeric(styled_df['proof'], errors='coerce')
if 'price' in styled_df.columns:
    styled_df['price'] = pd.to_numeric(styled_df['price'], errors='coerce')

odd_color  = "#1a1a1a"
even_color = "#2a2a2a"
text_color = "#eeeeee"

def color_rows(row):
    color = odd_color if row.name % 2 == 0 else even_color
    return [f"background-color: {color}; color: {text_color}"] * len(row)

reviewer_col_config = {
    c: st.column_config.NumberColumn(c.capitalize(), format="%.1f") for c in active_reviewers
}

edited_df = st.data_editor(
    display_df,
    column_order=[
        "select", "date", "link", "brand", "name", "avg", "score",
        *active_reviewers,
        "age", "proof", "price", "type"
    ],
    column_config={
        "select": st.column_config.CheckboxColumn("Select"),
        "date":   st.column_config.DateColumn("Date", format="DD MMMM YYYY"),
        "link":   st.column_config.LinkColumn("Video Link", display_text="▶ Watch"),
        "brand":  st.column_config.TextColumn("Brand"),
        "name":   st.column_config.TextColumn("Whiskey Name"),
        "avg":    st.column_config.NumberColumn("Avg Score", format="%.1f"),
        "score":  st.column_config.TextColumn("Verdict"),
        "age":    st.column_config.NumberColumn("Age"),
        "proof":  st.column_config.NumberColumn("Proof", format="%.1f"),
        "price":  st.column_config.NumberColumn("Price ($)", format="$%d"),
        "type":   st.column_config.TextColumn("Type"),
        **reviewer_col_config,
    },
    hide_index=True,
    use_container_width=True,
)

selected_rows = edited_df[edited_df["select"]]

if len(selected_rows) == 0:
    st.info("☝️ Check boxes above to select whiskeys you've tried.")
    st.stop()

if len(selected_rows) > 20:
    st.warning("⚠️ Please select no more than 20 observations.")
    st.stop()

# ── Reviewer averages for selected rows ───────────────────────────────────────
reviewer_avgs = selected_rows[active_reviewers].apply(
    pd.to_numeric, errors='coerce'
).mean(skipna=True).round(1)

st.subheader("Average Reviewer Scores for Selected Whiskeys")
st.table(reviewer_avgs.rename(index=lambda x: x.capitalize()).to_frame(name="Average Score"))
overall_avg = reviewer_avgs.mean().round(2)
st.markdown(f"**Overall Average Across All Reviewers:** `{overall_avg}`")

# ── User score sliders ────────────────────────────────────────────────────────
st.markdown("### Your Scores")
user_scores = []
cols = st.columns(3)
for i, (idx, row) in enumerate(selected_rows.iterrows()):
    with cols[i % 3]:
        user_score = st.slider(
            label=f"{row['brand']} — {row['name']}",
            min_value=0.0, max_value=10.0,
            step=0.1, value=5.0, format="%.1f",
            key=f"user_score_{idx}"
        )
        user_scores.append({"name": row["name"], "Reviewer": "you", "Score": user_score})

# ── Box plot comparison ───────────────────────────────────────────────────────
box_df = selected_rows.reset_index()[["name"] + active_reviewers].melt(
    id_vars=["name"], var_name="Reviewer", value_name="Score"
)
if user_scores:
    box_df = pd.concat([box_df, pd.DataFrame(user_scores)], ignore_index=True)

box_df['Reviewer'] = box_df['Reviewer'].str.capitalize()
box_df['Score'] = pd.to_numeric(box_df['Score'], errors='coerce')

fig = px.box(
    box_df, x="Reviewer", y="Score",
    points="all",
    title="Your Scores vs. the Crew",
    labels={"Score": "Score", "Reviewer": "Reviewer"},
    custom_data=["name"],
    color="Reviewer",
)
fig.update_traces(
    hovertemplate="Reviewer: %{x}<br>Score: %{y}<br>Whiskey: %{customdata[0]}<extra></extra>",
    marker=dict(line=dict(color='#c8640a', width=1)),
)
fig.update_layout(
    yaxis_range=[0, 10],
    showlegend=False,
    paper_bgcolor='#1a0a00',
    plot_bgcolor='#2d1400',
    font=dict(color='#f5e6d3', family='Source Sans 3'),
    title_font=dict(color='#ffd699', family='Playfair Display', size=18),
    xaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0', tickfont=dict(color='#f0d5b0')),
    yaxis=dict(gridcolor='#3a1800', linecolor='#7a3e00', tickcolor='#f0d5b0', tickfont=dict(color='#f0d5b0')),
)
# Amber/bourbon color sequence for reviewers
amber_colors = ['#c8640a','#f5a944','#7a3e00','#ffd699','#a0522d','#e8922a','#d4956a']
for i, trace in enumerate(fig.data):
    trace.marker.color = amber_colors[i % len(amber_colors)]
    trace.line.color   = amber_colors[i % len(amber_colors)]
st.plotly_chart(fig, use_container_width=True)

# ── Closest reviewer summary ──────────────────────────────────────────────────
if user_scores:
    st.subheader("🎯 Your Closest Match")
    user_df_lookup = pd.DataFrame(user_scores).set_index("name")["Score"]
    selected_named = selected_rows.set_index("name")

    diffs = {}
    for r in active_reviewers:
        col_data = pd.to_numeric(selected_named[r], errors='coerce').dropna()
        user_common = user_df_lookup.reindex(col_data.index).dropna()
        if not user_common.empty:
            diffs[r.capitalize()] = (col_data.reindex(user_common.index) - user_common).abs().mean()

    if diffs:
        closest = min(diffs, key=diffs.get)
        st.success(f"Based on your ratings, you align most closely with **{closest}** "
                   f"(avg difference: {diffs[closest]:.2f} points).")
        diff_df = pd.DataFrame(
            {"Reviewer": list(diffs.keys()), "Avg Score Difference": list(diffs.values())}
        ).sort_values("Avg Score Difference")
        st.dataframe(diff_df, hide_index=True, use_container_width=True)