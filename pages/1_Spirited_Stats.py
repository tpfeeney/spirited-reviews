import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def add_sidebar_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://raw.githubusercontent.com/tpfeeney/spirited-reviews/main/srlogo.png');
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

# Use the shared DataFrame
df = st.session_state.get("df")

# Sidebar: Properly capitalized options
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

# Prepare long format for boxplot
df_melted = df.melt(value_vars=['randy', 'norm', 'zach', 'justin'],
                    var_name='Person', value_name='Score')
df_melted['Person'] = df_melted['Person'].str.capitalize()  # Capitalize labels

# Coloring logic
# Get all unique people and sort for consistency
people = sorted(df_melted['Person'].unique())

# Generate pastel color palette and map to people
palette = sns.color_palette("pastel")
base_palette_dict = dict(zip(people, palette))

if selected_key == "overall":
    # Use all original pastel colors
    palette_dict = base_palette_dict
else:
    # Highlight selected person using their pastel color, others in gray
    palette_dict = {
        person: base_palette_dict[person] if person == selected_name else 'lightgray'
        for person in people
    }
    
# Plot boxplot
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_ylim(0, 10)
sns.boxplot(data=df_melted, x='Person', y='Score', ax=ax, palette=palette_dict)
ax.set_title("Score Distribution by Person")

st.pyplot(fig)