import streamlit as st
import pandas as pd
import numpy as np
from utils import add_sidebar_logo, get_data, REVIEWER_COLS

st.set_page_config(
    page_title="Spirited Reviews",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_sidebar_logo()

st.title("Spirited Reviews 🥃")

df = get_data()

# ── Sidebar controls ──────────────────────────────────────────────────────────
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    del st.session_state["df"]
    st.rerun()

theme = st.sidebar.radio("Table theme", ["Dark", "Light"], horizontal=True)

# ── Display table ─────────────────────────────────────────────────────────────
active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]
reviewer_display = {c: c.capitalize() for c in active_reviewers}

base_cols  = ["date", "link", "brand", "name", "avg", "score"]
tail_cols  = ["age", "proof", "price", "type"]
display_cols = base_cols + active_reviewers + tail_cols

display_df = df[[c for c in display_cols if c in df.columns]].copy()
display_df["date"] = display_df["date"].dt.strftime("%d %B %Y")

# Rename to display-friendly headers
rename_map = {
    "date": "Date", "link": "Video Link", "brand": "Brand",
    "name": "Whiskey Name", "avg": "Avg Score", "score": "Verdict",
    "age": "Age", "proof": "Proof", "price": "Price ($)", "type": "Type",
    **reviewer_display
}
display_df.rename(columns=rename_map, inplace=True)

reviewer_display_names = [reviewer_display[c] for c in active_reviewers]

if theme == "Dark":
    odd_color  = "#1a1a1a"
    even_color = "#2a2a2a"
    hover_color = "#3a3020"
else:
    odd_color  = "#ffffff"
    even_color = "#f2efe8"
    hover_color = "#fdf3dc"

display_df["Avg Score"] = pd.to_numeric(display_df["Avg Score"], errors="coerce")
for col in reviewer_display_names + ["Proof"]:
    if col in display_df.columns:
        display_df[col] = pd.to_numeric(display_df[col], errors="coerce")

# Compute median across active reviewer columns
display_df["Median Score"] = display_df[reviewer_display_names].median(axis=1, skipna=True).round(1)

# Insert Median Score right after Avg Score
cols = list(display_df.columns)
avg_idx = cols.index("Avg Score")
cols.insert(avg_idx + 1, cols.pop(cols.index("Median Score")))
display_df = display_df[cols]

# ── Pre-format columns as strings so Streamlit never renders "None" ───────────
# Numeric score columns → "6.5" or "—"
for col in reviewer_display_names + ["Avg Score", "Median Score"]:
    if col in display_df.columns:
        display_df[col] = display_df[col].apply(
            lambda x: f"{x:.1f}" if pd.notna(x) and x is not None else "—"
        )

# Age → "12 yr" or "NAS"
display_df["Age"] = display_df["Age"].apply(
    lambda x: f"{float(x):.0f} yr" if pd.notna(x) and x is not None else "NAS"
)

# Proof → "117.3" or "—"
if "Proof" in display_df.columns:
    display_df["Proof"] = display_df["Proof"].apply(
        lambda x: f"{x:.1f}" if pd.notna(x) and x is not None else "—"
    )

# Price → "$45" or "—"
display_df["Price ($)"] = display_df["Price ($)"].apply(
    lambda x: f"${float(x):.0f}" if pd.notna(x) and x is not None else "—"
)

text_color = "#eeeeee" if theme == "Dark" else "#222222"

def color_rows(row):
    color = odd_color if row.name % 2 == 0 else even_color
    return [f"background-color: {color}; color: {text_color}"] * len(row)

reviewer_fmt = {}

styled = (
    display_df.reset_index(drop=True).style
    .apply(color_rows, axis=1)
)

st.dataframe(
    styled,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Video Link": st.column_config.LinkColumn("Video Link", display_text="▶ Watch"),
        "Date":       st.column_config.TextColumn("Date"),
    }
)

# ── Scoring key ───────────────────────────────────────────────────────────────
with st.expander("📊 Scoring Key"):
    st.image(
        "https://github.com/tpfeeney/spirited-reviews/blob/main/Scoring_Sheet_Final.jpg?raw=true",
        caption="Spirited Reviews Scoring Guide",
        width=600
    )