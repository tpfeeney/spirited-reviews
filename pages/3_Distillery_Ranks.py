import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- Sidebar logo styling ---
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

# --- Load data ---
df = st.session_state.get("df")

if df is None or df.empty:
    st.error("No data found in session_state['df']. Please load data before using the app.")
    st.stop()

if 'type' not in df.columns:
    st.error("'type' column not found in the dataframe.")
    st.stop()

# --- Legacy distillery list ---
legacy_brands = [
    "Jack Daniel's", "Heaven Hill", "Jim Beam", "Bardstown", "Maker's Mark",
    "Wild Turkey", "Buffalo Trace", "Four Roses", "MGP",
    "Old Forester", "Willett"
]

# --- Sidebar controls ---
st.sidebar.header("Filters")

# Distillery type filter
distillery_option = st.sidebar.radio("Select Distillery Type:", ("All", "Legacy Distillery"))

# 'type' filter radio button
unique_types = sorted(df['type'].dropna().unique())
type_option = st.sidebar.radio("Restrict to Type:", options=["All Types"] + list(unique_types), index=0)

# Reviewer selection
reviewers = ['randy', 'norm', 'zach', 'justin']
selected_reviewers = []

st.sidebar.markdown("### Select Reviewers (including Overall)")
include_overall = st.sidebar.checkbox("Overall", value=True)
if include_overall:
    selected_reviewers.append('avg')

for reviewer in reviewers:
    if st.sidebar.checkbox(reviewer.capitalize(), value=True):
        selected_reviewers.append(reviewer)

# --- Filter data ---
df_filtered = df.copy()

if distillery_option == "Legacy Distillery":
    df_filtered = df_filtered[df_filtered['brand'].isin(legacy_brands)]

if type_option != "All Types":
    df_filtered = df_filtered[df_filtered['type'] == type_option]

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- Section 1: Average Score Table ---
st.header("Average Scores by Brand")

avg_cols = selected_reviewers.copy()

grouped = df_filtered.groupby('brand')[avg_cols].mean().reset_index()

# Calculate # of Reviews per brand
review_counts = df_filtered.groupby('brand').size().reset_index(name='# of Reviews')

# Merge # of Reviews into grouped data
grouped = pd.merge(grouped, review_counts, on='brand', how='left')

# Rename columns
rename_dict = {r: f"{r.capitalize()} Avg" if r != 'avg' else "Overall Avg" for r in avg_cols}
grouped.rename(columns=rename_dict, inplace=True)

# Sort by Overall Avg descending if present, else first avg column
sort_col = "Overall Avg" if "Overall Avg" in grouped.columns else grouped.columns[1]
grouped = grouped.round(2).sort_values(by=sort_col, ascending=False)
grouped.index = range(1, len(grouped) + 1)

# Format floats nicely
format_dict = {col: '{:.2f}' for col in grouped.columns if 'Avg' in col}
st.dataframe(grouped.style.format(format_dict))

# --- Section 2: Boxplot ---
if selected_reviewers:
    st.header("Score Distribution by Brand")

    df_melted = df_filtered[['brand'] + selected_reviewers].melt(
        id_vars='brand', var_name='Reviewer', value_name='Score'
    )
    df_melted['Reviewer'] = df_melted['Reviewer'].apply(lambda x: "Overall" if x == 'avg' else x.capitalize())

    fig, ax = plt.subplots(figsize=(6, 4))

    if set(df_melted['Reviewer']) == {"Overall"}:
        sns.boxplot(data=df_melted, x='brand', y='Score', color='skyblue', ax=ax)
    else:
        sns.boxplot(data=df_melted, x='brand', y='Score', hue='Reviewer', ax=ax, palette='pastel')

    title_suffix = f" — {type_option}" if type_option != "All Types" else ""
    ax.set_title(f"Boxplot of Scores by Brand{title_suffix}")
    ax.set_xlabel("Brand")
    ax.set_ylabel("Score")
    ax.tick_params(axis='x', rotation=45)
    if len(df_melted['Reviewer'].unique()) > 1:
        ax.legend(title="Reviewer", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)
else:
    st.warning("Please select at least one reviewer.")
