import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import add_sidebar_logo, get_data, score_label, REVIEWER_COLS

st.title("Find your Spirit Reviewer")
st.info(
    "Select whiskeys by checking the boxes, rate them yourself using the sliders, "
    "then see whose palate matches yours most closely."
)

add_sidebar_logo()

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]

# ── Editable table with select checkboxes ─────────────────────────────────────
display_df = df.copy()
if "select" not in display_df.columns:
    display_df["select"] = False

reviewer_col_config = {
    c: st.column_config.NumberColumn(c.capitalize()) for c in active_reviewers
}

edited_df = st.data_editor(
    display_df,
    column_order=[
        "select", "date", "link", "brand", "name", "avg", "score",
        *active_reviewers,
        "age", "proof", "price", "type"
    ],
    column_config={
        "select": st.column_config.CheckboxColumn("Select"),
        "date":   st.column_config.DateColumn("Date", format="DD MMMM YYYY"),
        "link":   st.column_config.LinkColumn("Video Link", display_text="Open Review"),
        "brand":  st.column_config.TextColumn("Brand"),
        "name":   st.column_config.TextColumn("Whiskey Name"),
        "avg":    st.column_config.NumberColumn("Average Score"),
        "score":  st.column_config.TextColumn("Verdict"),
        "age":    st.column_config.NumberColumn("Age"),
        "proof":  st.column_config.NumberColumn("Proof"),
        "price":  st.column_config.NumberColumn("Price ($)"),
        "type":   st.column_config.TextColumn("Type"),
        **reviewer_col_config,
    },
    hide_index=True,
    use_container_width=True,
)

selected_rows = edited_df[edited_df["select"]]

if len(selected_rows) == 0:
    st.info("☝️ Check boxes above to select whiskeys you've tried.")
    st.stop()

if len(selected_rows) > 20:
    st.warning("⚠️ Please select no more than 20 observations.")
    st.stop()

# ── Reviewer averages for selected rows ───────────────────────────────────────
reviewer_avgs = selected_rows[active_reviewers].apply(
    pd.to_numeric, errors='coerce'
).mean(skipna=True).round(1)

st.subheader("Average Reviewer Scores for Selected Whiskeys")
st.table(reviewer_avgs.rename(index=lambda x: x.capitalize()).to_frame(name="Average Score"))
overall_avg = reviewer_avgs.mean().round(2)
st.markdown(f"**Overall Average Across All Reviewers:** `{overall_avg}`")

# ── User score sliders ────────────────────────────────────────────────────────
st.markdown("### Your Scores")
user_scores = []
cols = st.columns(3)
for i, (idx, row) in enumerate(selected_rows.iterrows()):
    with cols[i % 3]:
        user_score = st.slider(
            label=f"{row['brand']} — {row['name']}",
            min_value=0.0, max_value=10.0,
            step=0.1, value=5.0, format="%.1f",
            key=f"user_score_{idx}"
        )
        user_scores.append({"name": row["name"], "Reviewer": "you", "Score": user_score})

# ── Box plot comparison ───────────────────────────────────────────────────────
box_df = selected_rows.reset_index()[["name"] + active_reviewers].melt(
    id_vars=["name"], var_name="Reviewer", value_name="Score"
)
if user_scores:
    box_df = pd.concat([box_df, pd.DataFrame(user_scores)], ignore_index=True)

box_df['Reviewer'] = box_df['Reviewer'].str.capitalize()
box_df['Score'] = pd.to_numeric(box_df['Score'], errors='coerce')

fig = px.box(
    box_df, x="Reviewer", y="Score",
    points="all",
    title="Your Scores vs. the Crew",
    labels={"Score": "Score", "Reviewer": "Reviewer"},
    custom_data=["name"],
    color="Reviewer",
)
fig.update_traces(
    hovertemplate="Reviewer: %{x}<br>Score: %{y}<br>Whiskey: %{customdata[0]}<extra></extra>"
)
fig.update_layout(yaxis_range=[0, 10], showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ── Closest reviewer summary ──────────────────────────────────────────────────
if user_scores:
    st.subheader("🎯 Your Closest Match")
    user_df_lookup = pd.DataFrame(user_scores).set_index("name")["Score"]
    selected_named = selected_rows.set_index("name")

    diffs = {}
    for r in active_reviewers:
        col_data = pd.to_numeric(selected_named[r], errors='coerce').dropna()
        user_common = user_df_lookup.reindex(col_data.index).dropna()
        if not user_common.empty:
            diffs[r.capitalize()] = (col_data.reindex(user_common.index) - user_common).abs().mean()

    if diffs:
        closest = min(diffs, key=diffs.get)
        st.success(f"Based on your ratings, you align most closely with **{closest}** "
                   f"(avg difference: {diffs[closest]:.2f} points).")
        diff_df = pd.DataFrame(
            {"Reviewer": list(diffs.keys()), "Avg Score Difference": list(diffs.values())}
        ).sort_values("Avg Score Difference")
        st.dataframe(diff_df, hide_index=True, use_container_width=True)