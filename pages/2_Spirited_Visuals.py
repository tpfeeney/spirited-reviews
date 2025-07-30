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
if 'age_new' not in page_df.columns:
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
    ["Proof Breakdown", "Type Breakdown", "Price v Review", "Proof v Review", "Age v Review", "Choose your own adventure"]
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
    

elif chart_type == "Choose your own adventure":
    st.sidebar.markdown("### Select X and Y axes")

    all_options = {
        "avg": "Overall Average",
        "age_new": "Age",
        "price": "Price ($)",
        "proof": "Proof",
        "randy": "Randy Score",
        "norm": "Norm Score",
        "justin": "Justin Score",
        "zach": "Zach Score"
    }

    allowed_keys = list(all_options.keys())

    # Default X axis variable
    default_x = "price"
    if default_x not in allowed_keys:
        default_x = allowed_keys[0]

    # Select X axis
    x_col_key = st.sidebar.selectbox(
        "X-axis:",
        options=allowed_keys,
        index=allowed_keys.index(default_x),
        format_func=lambda x: all_options[x]
    )

    # Y axis options exclude the chosen X axis
    y_options = [k for k in allowed_keys if k != x_col_key]

    # Default Y axis variable is 'avg' if available
    if "avg" in y_options:
        default_y = "avg"
    else:
        default_y = y_options[0]

    # Select Y axis
    y_col_key = st.sidebar.selectbox(
        "Y-axis:",
        options=y_options,
        index=y_options.index(default_y),
        format_func=lambda x: all_options[x]
    )

    # Sidebar: Choose trendline type
    trendline_option = st.sidebar.radio(
        "Add Trendline",
        options=["None", "OLS", "LOWESS"],
        index=1  # Default to "OLS"
    )

    # Map user-friendly names to plotly options
    trendline_map = {
        "None": None,
        "OLS": "ols",
        "LOWESS": "lowess"
    }

    # Plotting
    fig = px.scatter(
        page_df,
        x=x_col_key,
        y=y_col_key,
        trendline=trendline_map[trendline_option],
        labels={
            x_col_key: all_options[x_col_key],
            y_col_key: all_options[y_col_key]
        },
        title=f"{all_options[y_col_key]} vs {all_options[x_col_key]}",
        hover_name="name"
    )
    
    st.plotly_chart(fig, use_container_width=True)