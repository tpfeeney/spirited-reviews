import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

st.title("Spirited Stats")

# --- Load data ---
df = st.session_state.get("df")

if df is None or df.empty:
    st.error("No data found in session_state['df']. Please load data before using the app.")
    st.stop()

# --- Add 'type' filter radio in sidebar ---
if 'type' in df.columns and not df['type'].dropna().empty:
    unique_types = sorted(df['type'].dropna().unique())
    type_option = st.sidebar.radio("Restrict to Type:", options=["All Types"] + unique_types, index=0)
else:
    type_option = "All Types"

# --- Filter dataframe by selected type ---
if type_option != "All Types":
    df = df[df['type'] == type_option]

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Sidebar: Properly capitalized options for reviewers
raw_names = ['overall', 'randy', 'norm', 'zach', 'justin']
name_options = [name.capitalize() for name in raw_names]
selected_name = st.sidebar.radio("Select Person", name_options)
selected_key = selected_name.lower()  # For indexing

# Metrics logic
if selected_key == "overall":
    scores = df['avg']
else:
    scores = df[selected_key]

# First row of metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Rev", value=f"{scores.count():}")
with col2:
    st.metric(label="Min Score", value=f"{scores.min():.2f}")
with col3:
    st.metric(label="Avg Score", value=f"{scores.mean():.2f}")
with col4:
    st.metric(label="Max Score", value=f"{scores.max():.2f}")

# Second row of metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="", value="")
with col2:
    st.metric(label="25% Percentile", value=f"{scores.quantile(0.25):.2f}")
with col3:
    st.metric(label="Median", value=f"{scores.median():.2f}")
with col4:
    st.metric(label="75% Percentile", value=f"{scores.quantile(0.75):.2f}")

# Prepare long format for boxplot (only reviewers)
df_melted = df.melt(value_vars=['randy', 'norm', 'zach', 'justin'],
                    var_name='Person', value_name='Score')
df_melted['Person'] = df_melted['Person'].str.capitalize()  # Capitalize labels

# Coloring logic
people = sorted(df_melted['Person'].unique())
palette = sns.color_palette("pastel")
base_palette_dict = dict(zip(people, palette))

if selected_key == "overall":
    # Use all pastel colors
    palette_dict = base_palette_dict
else:
    # Highlight selected person, gray others
    palette_dict = {
        person: base_palette_dict[person] if person == selected_name else 'lightgray'
        for person in people
    }
    
# Plot boxplot
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_ylim(0, 10)
sns.boxplot(data=df_melted, x='Person', y='Score', ax=ax, palette=palette_dict)
ax.set_title(f"Score Distribution by Person — {type_option}")
st.pyplot(fig)
