import streamlit as st
import pandas as pd
import plotly.express as px
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

add_sidebar_logo()

st.title("Spirited Visualizations")

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]

# ── Data prep ─────────────────────────────────────────────────────────────────
page_df = df.copy()
page_df['age_new'] = pd.to_numeric(page_df['age'], errors='coerce')
page_df['avg']     = pd.to_numeric(page_df['avg'],   errors='coerce')
page_df['proof']   = pd.to_numeric(page_df['proof'], errors='coerce')
page_df['price']   = pd.to_numeric(page_df['price'], errors='coerce')
for c in active_reviewers:
    page_df[c] = pd.to_numeric(page_df[c], errors='coerce')

bins   = [79, 89, 94, 99, 104, 109, 114, 119, 129, 139, 149, float('inf')]
labels = ["80-89","90-94","95-99","100-104","105-109",
          "110-114","115-119","120-129","130-139","140-149",">=150"]
page_df['proof_cat'] = pd.cut(page_df['proof'], bins=bins, labels=labels, right=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
chart_type = st.sidebar.radio(
    "Select chart type:",
    ["Proof Breakdown", "Type Breakdown", "Price v Review",
     "Proof v Review", "Age v Review", "Choose your own adventure"]
)

# ── Charts ────────────────────────────────────────────────────────────────────
if chart_type == "Proof Breakdown":
    proof_df = page_df['proof_cat'].value_counts().sort_index().reset_index()
    proof_df.columns = ['Proof Category', 'Count']
    fig = px.bar(proof_df, x='Proof Category', y='Count',
                 title="Number of Observations per Proof Category",
                 text='Count', color='Proof Category')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, showlegend=False,
                      margin=dict(t=60, b=80), height=500)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Type Breakdown":
    type_counts = page_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.pie(type_counts, names='type', values='count',
                 title="Distribution of Whiskey Types")
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
    age_df = page_df[page_df['age_new'].notna()]
    fig = px.scatter(age_df, x="age_new", y="avg", trendline="ols",
                     labels={"avg": "Average Rating", "age_new": "Age"},
                     hover_name="name")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Choose your own adventure":
    st.sidebar.markdown("### Select X and Y axes")

    all_options = {
        "avg":     "Overall Average",
        "age_new": "Age",
        "price":   "Price ($)",
        "proof":   "Proof",
        **{c: f"{c.capitalize()} Score" for c in active_reviewers},
    }
    allowed_keys = list(all_options.keys())

    x_col_key = st.sidebar.selectbox(
        "X-axis:", options=allowed_keys,
        index=allowed_keys.index("price"),
        format_func=lambda x: all_options[x]
    )
    y_options = [k for k in allowed_keys if k != x_col_key]
    y_col_key = st.sidebar.selectbox(
        "Y-axis:", options=y_options,
        index=y_options.index("avg") if "avg" in y_options else 0,
        format_func=lambda x: all_options[x]
    )
    trendline_option = st.sidebar.radio(
        "Add Trendline", options=["None", "OLS", "LOWESS"], index=1
    )
    trendline_map = {"None": None, "OLS": "ols", "LOWESS": "lowess"}

    fig = px.scatter(
        page_df, x=x_col_key, y=y_col_key,
        trendline=trendline_map[trendline_option],
        labels={x_col_key: all_options[x_col_key], y_col_key: all_options[y_col_key]},
        title=f"{all_options[y_col_key]} vs {all_options[x_col_key]}",
        hover_name="name"
    )
    st.plotly_chart(fig, use_container_width=True)