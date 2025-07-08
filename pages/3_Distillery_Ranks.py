import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load data ---
# Use the shared DataFrame
df = st.session_state.get("df")


# --- Legacy distillery list ---
legacy_brands = [
    "Jack Daniel's", "Heaven Hill", "Jim Beam", "Bardstown", "Maker's Mark",
    "Wild Turkey", "Buffalo Trace", "Four Roses", "MGP",
    "Old Forester", "Willett"
]

# --- Sidebar controls ---
st.sidebar.header("Filters")

distillery_option = st.sidebar.radio("Select Distillery Type:", ("All", "Legacy Distillery"))

reviewers = ['randy', 'norm', 'zach', 'justin']
selected_reviewers = []

st.sidebar.markdown("### Select Reviewers")
for reviewer in reviewers:
    if st.sidebar.checkbox(reviewer.capitalize(), value=True):
        selected_reviewers.append(reviewer)

# --- Filter dataset ---
if distillery_option == "Legacy Distillery":
    df_filtered = df[df['brand'].isin(legacy_brands)]
else:
    df_filtered = df.copy()

# --- Section 1: Average Score Table ---
st.header("Average Scores by Brand")

avg_cols = ['avg', 'randy', 'norm', 'zach', 'justin']
grouped = df_filtered.groupby('brand')[avg_cols].mean().reset_index()

grouped.rename(columns={
    'avg': 'Overall Avg',
    'randy': 'Randy Avg',
    'norm': 'Norm Avg',
    'zach': 'Zach Avg',
    'justin': 'Justin Avg'
}, inplace=True)

grouped = grouped.round(2)
grouped = grouped.sort_values(by='Overall Avg', ascending=False)
grouped.index = range(1, len(grouped) + 1)

st.dataframe(grouped.style.format({
    'Overall Avg': '{:.2f}',
    'Randy Avg': '{:.2f}',
    'Norm Avg': '{:.2f}',
    'Zach Avg': '{:.2f}',
    'Justin Avg': '{:.2f}'
}))

# --- Section 2: Boxplot ---
if selected_reviewers and not df_filtered.empty:
    st.header("Score Distribution by Brand")

    df_melted = df_filtered[['brand'] + selected_reviewers].melt(
        id_vars='brand', var_name='Reviewer', value_name='Score'
    )
    df_melted['Reviewer'] = df_melted['Reviewer'].str.capitalize()

    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(data=df_melted, x='brand', y='Score', hue='Reviewer', ax=ax, palette='pastel')
    ax.set_title("Boxplot of Scores by Brand and Reviewer")
    ax.set_xlabel("Brand")
    ax.set_ylabel("Score")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Reviewer", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)
else:
    st.warning("Please select at least one reviewer and ensure data is available.")
