import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load data ---
@st.cache_data
def load_data():
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

df = load_data()

# --- Create proof_cat buckets ---
proof_bins = [80, 90, 95, 100, 105, 110, 115, 120, 130, 140, 150, float('inf')]
proof_labels = ["80–89", "90–94", "95–99", "100–104", "105–109",
                "110–114", "115–119", "120–129", "130–139", "140–149", "150+"]

df['proof_cat'] = pd.cut(df['proof'], bins=proof_bins, labels=proof_labels, right=False)

# --- Sidebar filters ---
st.sidebar.header("Filters")

reviewers = ['randy', 'norm', 'zach', 'justin']
reviewer_options = ["Overall"] + reviewers
selected_reviewer = st.sidebar.selectbox(
    "Reviewer",
    reviewer_options,
    format_func=lambda x: x.capitalize() if x != "Overall" else "Overall"
)

# Type filter
types = sorted(df['type'].dropna().unique())
selected_types = st.sidebar.multiselect("Type", options=types)

# Brand filter
brands = sorted(df['brand'].dropna().unique())
selected_brands = st.sidebar.multiselect("Brand", options=brands)

# Age slider
if 'age' in df.columns and pd.api.types.is_numeric_dtype(df['age']):
    min_age, max_age = int(df['age'].min()), int(df['age'].max())
    selected_age = st.sidebar.slider("Age", min_value=min_age, max_value=max_age, value=(min_age, max_age))
else:
    selected_age = None

# Price slider
if 'price' in df.columns and pd.api.types.is_numeric_dtype(df['price']):
    min_price, max_price = int(df['price'].min()), int(df['price'].max())
    selected_price = st.sidebar.slider("Price", min_value=min_price, max_value=max_price, value=(min_price, max_price))
else:
    selected_price = None

# Proof checkbox filter
st.sidebar.markdown("Proof Range (select one or more):")
proof_cats = df['proof_cat'].dropna().unique().tolist()
proof_cats = sorted(proof_cats, key=lambda x: proof_labels.index(str(x)))

selected_proof_cats = []
for proof_cat in proof_cats:
    if st.sidebar.checkbox(str(proof_cat), value=True):
        selected_proof_cats.append(proof_cat)

# --- Filter the DataFrame ---
filtered_df = df.copy()

if selected_types:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]

if selected_brands:
    filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]

if selected_age:
    filtered_df = filtered_df[(filtered_df['age'] >= selected_age[0]) & (filtered_df['age'] <= selected_age[1])]

if selected_price:
    filtered_df = filtered_df[(filtered_df['price'] >= selected_price[0]) & (filtered_df['price'] <= selected_price[1])]

if selected_proof_cats:
    filtered_df = filtered_df[filtered_df['proof_cat'].isin(selected_proof_cats)]

# --- Plotting ---
st.header("Score Distribution")

if filtered_df.empty:
    st.warning("No data available with the selected filters.")
else:
    if selected_reviewer == "Overall":
        # Overall avg scores boxplot
        df_plot = filtered_df[['brand', 'avg']].copy()
        df_plot.rename(columns={'avg': 'Score'}, inplace=True)
        x_axis = 'brand'
        title = "Overall Average Scores by Brand"

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df_plot, x=x_axis, y='Score', ax=ax, palette='pastel')
        ax.set_title(title)
        ax.set_xlabel(x_axis.capitalize())
        ax.set_ylabel("Average Score")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    else:
        # Specific reviewer boxplot
        reviewer_col = selected_reviewer.lower()
        if reviewer_col not in filtered_df.columns:
            st.error(f"Reviewer column '{reviewer_col}' not found in data.")
        else:
            df_plot = filtered_df[['brand', reviewer_col]].copy()
            df_plot.rename(columns={reviewer_col: 'Score'}, inplace=True)
            df_plot['Reviewer'] = selected_reviewer.capitalize()
            x_axis = 'brand'
            title = f"{selected_reviewer.capitalize()} Scores by Brand"

            fig, ax = plt.subplots(figsize=(12, 6))
            sns.boxplot(data=df_plot, x=x_axis, y='Score', ax=ax, palette='pastel')
            ax.set_title(title)
            ax.set_xlabel(x_axis.capitalize())
            ax.set_ylabel("Score")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
