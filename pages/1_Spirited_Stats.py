import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

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

fig, ax = plt.subplots(figsize=(max(10, len(people) * 1.5), 5))
ax.set_ylim(0, 10)
sns.boxplot(data=df_melted, x='Person', y='Score', ax=ax, palette=palette_dict)
ax.set_title(f"Score Distribution by Person — {type_option}")
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)