import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Load data ---
df = st.session_state.get("df")

# Make a copy to avoid modifying shared session state
page_df = df.copy()

# Clean and convert fields just for this page
page_df['age_new'] = (
    page_df['age']
    .astype(str)
    .str.replace(' Years', '', regex=False)
    .replace('NAS', pd.NA)
)
page_df['age_new'] = pd.to_numeric(page_df['age_new'], errors='coerce')

page_df['price'] = pd.to_numeric(page_df['price'].replace('[\$,]', '', regex=True), errors='coerce')
page_df['avg'] = pd.to_numeric(page_df['avg'], errors='coerce')
page_df['proof'] = pd.to_numeric(page_df['proof'], errors='coerce')

# Create proof_cat variable
bins = [79, 89, 94, 99, 104, 109, 114, 119, 129, 139, 149, float('inf')]
labels = [
    "80-89", "90-94", "95-99", "100-104", "105-109",
    "110-114", "115-119", "120-129", "130-139", "140-149", ">=150"
]
page_df['proof_cat'] = pd.cut(page_df['proof'], bins=bins, labels=labels, right=True)
cat_counts = page_df['proof_cat'].value_counts().sort_index()

# Sidebar chart selection
chart_type = st.sidebar.radio(
    "Select chart type:",
    ["Proof Breakdown", "Type Breakdown", "Price v Review", "Proof v Review", "Age v Review"]
)

st.title("Spirited Visualizations")

# ---------------------- Chart Logic ----------------------

if chart_type == "Proof Breakdown":
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_xlabel("Proof Category")
    ax.set_ylabel("Count")
    ax.set_title("Number of Observations per Proof Category")
    ax.set_xticklabels(cat_counts.index, rotation=45, ha='right')
    st.pyplot(fig)

elif chart_type == "Type Breakdown":
    type_counts = page_df['type'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Make it a circle
    ax.set_title("Distribution of Whiskey Types")
    st.pyplot(fig)

elif chart_type == "Price v Review":
    fig = px.scatter(page_df, x="price", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "price": "Price ($)"},
                     hover_name="name")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Proof v Review":
    fig = px.scatter(page_df, x="proof", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "proof": "Proof"},
                     hover_name="name")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Age v Review":
    age_filtered_df = page_df[page_df['age_new'].notna()]
    fig = px.scatter(age_filtered_df, x="age_new", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "age_new": "Age"},
                     hover_name="name")
    st.plotly_chart(fig, use_container_width=True)
