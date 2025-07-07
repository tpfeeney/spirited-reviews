import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load data ---
@st.cache_data
def load_data():
    # Replace with your actual data source
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

df = load_data()



bins = [79, 89, 94, 99, 104, 109, 114, 119, 129, 139, 149, float('inf')]
labels = [
    "80-89", "90-94", "95-99", "100-104", "105-109",
    "110-114", "115-119", "120-129", "130-139", "140-149", ">=150"
]


# Create proof_cat variable
df['proof_cat'] = pd.cut(df['proof'], bins=bins, labels=labels, right=True)

# Count number of rows in each category
cat_counts = df['proof_cat'].value_counts().sort_index()
# Sidebar chart selection
chart_type = st.sidebar.radio("Select chart type:", ["Proof Breakdown", "Type Breakdown"])

st.title("Spirited Visualizations")

if chart_type == "Proof Breakdown":
    # Define bins and labels
    bins = [79, 89, 94, 99, 104, 109, 114, 119, 129, 139, 149, float('inf')]
    labels = [
        "80-89", "90-94", "95-99", "100-104", "105-109",
        "110-114", "115-119", "120-129", "130-139", "140-149", ">=150"
    ]

    # Create binned category
    df['proof_cat'] = pd.cut(df['proof'], bins=bins, labels=labels, right=True)
    cat_counts = df['proof_cat'].value_counts().sort_index()

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_xlabel("Proof Category")
    ax.set_ylabel("Count")
    ax.set_title("Number of Observations per Proof Category")
    ax.set_xticklabels(cat_counts.index, rotation=45, ha='right')

    st.pyplot(fig)

elif chart_type == "Type Breakdown":
    type_counts = df['type'].value_counts()

    # Plot pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Make it a circle
    ax.set_title("Distribution of Whiskey Types")

    st.pyplot(fig)