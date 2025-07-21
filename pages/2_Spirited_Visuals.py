import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
    cat_counts = page_df['proof_cat'].value_counts().sort_index()
    proof_df = cat_counts.reset_index()
    proof_df.columns = ['Proof Category', 'Count']

    fig = px.bar(
        proof_df,
        x='Proof Category',
        y='Count',
        title="Number of Observations per Proof Category",
        labels={'Count': 'Count', 'Proof Category': 'Proof Category'},
        text='Count',
        color='Proof Category'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        margin=dict(t=60, b=80),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Type Breakdown":
    type_counts = page_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    
    fig = px.pie(
        type_counts,
        names='type',
        values='count',
        title="Distribution of Whiskey Types"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

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
