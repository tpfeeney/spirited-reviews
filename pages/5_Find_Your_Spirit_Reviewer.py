import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import plotly.express as px

st.title("Find your Spirit Reviewer")

st.info("Select observations (up to 10) by checking the boxes and then providing your own reviews below to see how your favorites align with Randy, Norm, Zach and Justin below. This, we hope, will help you find the reviewer most aligned with your palate.")

def score_label(avg):
    if 0 < avg < 1:
        return "tainted, WTF?!"
    elif 1 <= avg < 2:
        return "Dumpster Fire Adjacent"
    elif 2 <= avg < 3:
        return "Tastes Like Regret"
    elif 3 <= avg < 4:
        return "Last call material"
    elif 4 <= avg < 5:
        return "Questionable Choices"
    elif 5 <= avg < 6:
        return "Has Potential..."
    elif 6 <= avg < 7:
        return "Weeknight Winner"
    elif 7 <= avg < 8:
        return "Shelf-Worthy"
    elif 8 <= avg < 9:
        return "Hello There"
    elif 9 <= avg < 10:
        return "Legen...Wait For It..Dary!"
    elif avg >= 10:
        return "Flawless Victory"
    else:
        return np.nan
        
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

@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    
    # Parse dates and filter
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  
    today = pd.Timestamp.today().normalize()
    df = df[df['date'] <= today - pd.Timedelta(days=2)]
    
    # Compute average score across non-null reviewer columns
    reviewer_cols = ['randy', 'norm', 'zach', 'justin']
    df['avg'] = df[reviewer_cols].mean(axis=1, skipna=True).round(1)
    
    # Relabel score
    df['score'] = df['avg'].apply(score_label)

    return df

# --- Load into session state ---
if "df" not in st.session_state:
    st.session_state.df = load_data()

# Copy dataframe to avoid modifying session state directly
df = st.session_state.df.copy()

# Add "select" column if not present
if "select" not in df.columns:
    df["select"] = False

# Display editable data editor with select checkboxes
edited_df = st.data_editor(
    df,
    column_order=[
        "select", "date", "link", "brand", "name", "avg", "score",
        "randy", "norm", "zach", "justin",
        "age", "proof", "price", "type"
    ],
    column_config={
        "select": st.column_config.CheckboxColumn("Select"),
        "date": st.column_config.DateColumn("Date", format="DD MMMM YYYY"),
        "link": st.column_config.LinkColumn("Video Link", display_text="Open Review"),
        "brand": st.column_config.TextColumn("Brand"),
        "name": st.column_config.TextColumn("Whiskey Name"),
        "avg": st.column_config.NumberColumn("Average Score"),
        "score": st.column_config.TextColumn("Verdict"),
        "randy": st.column_config.NumberColumn("Randy"),
        "norm": st.column_config.NumberColumn("Norm"),
        "zach": st.column_config.NumberColumn("Zach"),
        "justin": st.column_config.NumberColumn("Justin"),
        "age": st.column_config.NumberColumn("Age"),
        "proof": st.column_config.NumberColumn("Proof"),
        "price": st.column_config.NumberColumn("Price ($)"),
        "type": st.column_config.TextColumn("Type"),
    },
    hide_index=True,
    use_container_width=True
)


selected_rows = edited_df[edited_df["select"]]

if len(selected_rows) == 0:
    st.info("Select observations by checking the boxes above to see average reviewer scores.")
elif len(selected_rows) > 10:
    st.warning("⚠️ Please select no more than 10 observations.")
else:
    reviewer_cols = ["randy", "norm", "zach", "justin"]
    reviewer_avgs = selected_rows[reviewer_cols].mean(skipna=True).round(1)

    st.subheader("Average Reviewer Scores for Selected Observations")
    st.table(reviewer_avgs.to_frame(name="Average Score"))

    overall_avg = reviewer_avgs.mean().round(2)
    st.markdown(f"**Overall Average Across All Reviewers:** `{overall_avg}`")

st.markdown("### Your Scores")
user_scores = []

cols = st.columns(3)  # Create three columns
for i, (idx, row) in enumerate(selected_rows.iterrows()):
    col = cols[i % 3]  # Rotate through the 3 columns
    with col:
        user_score = st.slider(
            label=f"{row['brand']} {row['name']}",
            min_value=0.0,
            max_value=10.0,
            step=0.1,
            value=5.0,  # Default value
            format="%.1f",
            key=f"user_score_{idx}"
        )
        user_scores.append({
            "name": row["name"],
            "Reviewer": "you",
            "Score": user_score
        })

# Now, **after** the loop, prepare the box plot data
if len(selected_rows) > 0:
    reviewer_cols = ["randy", "norm", "zach", "justin"]

    box_df = selected_rows.reset_index()[["name"] + reviewer_cols].melt(
        id_vars=["name"], var_name="Reviewer", value_name="Score"
    )

    # Add user scores to the melted DataFrame
    if user_scores:
        user_df = pd.DataFrame(user_scores)
        box_df = pd.concat([box_df, user_df], ignore_index=True)

    fig = px.box(
        box_df,
        x="Reviewer",
        y="Score",
        points="all",
        title="Reviewer Score Distribution for Selected Observations",
        labels={"Score": "Score", "Reviewer": "Reviewer"},
        custom_data=["name"]
    )

    fig.update_traces(
        hovertemplate="Reviewer: %{x}<br>Score: %{y}<br>Name: %{customdata[0]}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)
