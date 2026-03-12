import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from utils import add_sidebar_logo, get_data, GUEST_COLS

st.set_page_config(
    page_title="Spirited Guests",
    page_icon="🍶",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_sidebar_logo()

st.title("Spirited Guests 🍶")

df = get_data()

if df is None or df.empty:
    st.error("No data available. Please return to the main page.")
    st.stop()

active_guests = [c for c in GUEST_COLS if c in df.columns]

if not active_guests:
    st.warning("No guest reviewer data found in the dataset.")
    st.stop()

# Only rows where at least one guest has scored
for col in active_guests:
    df[col] = pd.to_numeric(df[col], errors='coerce')

guest_df = df[df[active_guests].notna().any(axis=1)].copy()

if guest_df.empty:
    st.info("No reviews with guest scores yet.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
theme = st.sidebar.radio("Table theme", ["Dark", "Light"], horizontal=True)

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    del st.session_state["df"]
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — REVIEWS TABLE (guest columns only)
# ══════════════════════════════════════════════════════════════════════════════
st.header("Guest Reviews 🥃")

guest_display = {c: c.capitalize() for c in active_guests}

base_cols    = ["date", "link", "brand", "name"]
tail_cols    = ["age", "proof", "price", "type"]
display_cols = base_cols + active_guests + tail_cols

display_df = guest_df[[c for c in display_cols if c in guest_df.columns]].copy()
display_df["date"] = display_df["date"].dt.strftime("%d %B %Y")

rename_map = {
    "date": "Date", "link": "Video Link", "brand": "Brand",
    "name": "Whiskey Name", "age": "Age", "proof": "Proof",
    "price": "Price ($)", "type": "Type",
    **guest_display
}
display_df.rename(columns=rename_map, inplace=True)

guest_display_names = [guest_display[c] for c in active_guests]

# Compute guest avg and median
numeric_guests = display_df[guest_display_names].apply(pd.to_numeric, errors='coerce')
display_df["Guest Avg"]    = numeric_guests.mean(axis=1, skipna=True).round(1)
display_df["Guest Median"] = numeric_guests.median(axis=1, skipna=True).round(1)

# Insert Guest Avg and Median right after Whiskey Name
cols = list(display_df.columns)
name_idx = cols.index("Whiskey Name")
for insert_col in ["Guest Median", "Guest Avg"]:
    cols.insert(name_idx + 1, cols.pop(cols.index(insert_col)))
display_df = display_df[cols]

if theme == "Dark":
    odd_color  = "#1a1a1a"
    even_color = "#2a2a2a"
    text_color = "#eeeeee"
else:
    odd_color  = "#ffffff"
    even_color = "#f2efe8"
    text_color = "#222222"

# Format columns
for col in guest_display_names + ["Guest Avg", "Guest Median"]:
    if col in display_df.columns:
        display_df[col] = pd.to_numeric(display_df[col], errors='coerce').apply(
            lambda x: f"{x:.1f}" if pd.notna(x) else "—"
        )

if "Proof" in display_df.columns:
    display_df["Proof"] = pd.to_numeric(display_df["Proof"], errors='coerce').apply(
        lambda x: f"{x:.1f}" if pd.notna(x) else "—"
    )

display_df["Age"] = display_df["Age"].apply(
    lambda x: f"{float(x):.0f} yr" if pd.notna(x) and str(x) not in ('nan', '—') else "NAS"
)
display_df["Price ($)"] = display_df["Price ($)"].apply(
    lambda x: f"${float(x):.0f}" if pd.notna(x) and str(x) not in ('nan', '—') else "—"
)

def color_rows(row):
    color = odd_color if row.name % 2 == 0 else even_color
    return [f"background-color: {color}; color: {text_color}"] * len(row)

styled = display_df.reset_index(drop=True).style.apply(color_rows, axis=1)

st.dataframe(
    styled,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Video Link": st.column_config.LinkColumn("Video Link", display_text="▶ Watch"),
        "Date":       st.column_config.TextColumn("Date"),
    }
)

with st.expander("📊 Scoring Key"):
    st.image(
        "https://github.com/tpfeeney/spirited-reviews/blob/main/Scoring_Sheet_Final.jpg?raw=true",
        caption="Spirited Reviews Scoring Guide",
        width=600
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — STATS
# ══════════════════════════════════════════════════════════════════════════════
st.header("Guest Stats 📊")

if 'type' in guest_df.columns and not guest_df['type'].dropna().empty:
    unique_types = sorted(guest_df['type'].dropna().unique())
    type_option = st.sidebar.radio("Restrict to Type:", ["All Types"] + unique_types, index=0)
else:
    type_option = "All Types"

stats_df = guest_df.copy()
if type_option != "All Types":
    stats_df = stats_df[stats_df['type'] == type_option]

if stats_df.empty:
    st.warning("No data available for the selected type filter.")
else:
    name_options = ["Overall"] + [c.capitalize() for c in active_guests]
    selected_name = st.sidebar.radio("Select Guest", name_options)
    selected_key  = selected_name.lower()

    guest_avg_series = stats_df[active_guests].mean(axis=1, skipna=True).round(1)
    scores = guest_avg_series if selected_key == "overall" else stats_df[selected_key]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reviews",  int(scores.count()))
    c2.metric("Min Score",      f"{scores.min():.2f}")
    c3.metric("Avg Score",      f"{scores.mean():.2f}")
    c4.metric("Max Score",      f"{scores.max():.2f}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("", "")
    c2.metric("25th Percentile", f"{scores.quantile(0.25):.2f}")
    c3.metric("Median",          f"{scores.median():.2f}")
    c4.metric("75th Percentile", f"{scores.quantile(0.75):.2f}")

    df_melted = stats_df.melt(value_vars=active_guests, var_name='Guest', value_name='Score')
    df_melted['Guest'] = df_melted['Guest'].str.capitalize()

    guests_list  = sorted(df_melted['Guest'].unique())
    base_palette = dict(zip(guests_list, sns.color_palette("pastel", n_colors=len(guests_list))))
    palette_dict = base_palette if selected_key == "overall" else {
        g: base_palette[g] if g == selected_name else 'lightgray' for g in guests_list
    }

    fig, ax = plt.subplots(figsize=(max(8, len(guests_list) * 1.5), 5))
    ax.set_ylim(0, 10)
    sns.boxplot(data=df_melted, x='Guest', y='Score', ax=ax, palette=palette_dict)
    ax.set_title(f"Score Distribution by Guest — {type_option}")
    ax.tick_params(axis='x', rotation=30)
    st.pyplot(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — FIND YOUR GUEST REVIEWER
# ══════════════════════════════════════════════════════════════════════════════
st.header("Find Your Guest Reviewer 🎯")
st.info(
    "Select whiskeys by checking the boxes, rate them yourself using the sliders, "
    "then see which guest reviewer's palate matches yours most closely."
)

pick_df = guest_df.copy()
if "select" not in pick_df.columns:
    pick_df["select"] = False

edited_df = st.data_editor(
    pick_df,
    column_order=[
        "select", "date", "link", "brand", "name",
        *active_guests,
        "age", "proof", "price", "type"
    ],
    column_config={
        "select": st.column_config.CheckboxColumn("Select"),
        "date":   st.column_config.DateColumn("Date", format="DD MMMM YYYY"),
        "link":   st.column_config.LinkColumn("Video Link", display_text="Open Review"),
        "brand":  st.column_config.TextColumn("Brand"),
        "name":   st.column_config.TextColumn("Whiskey Name"),
        "age":    st.column_config.NumberColumn("Age"),
        "proof":  st.column_config.NumberColumn("Proof"),
        "price":  st.column_config.NumberColumn("Price ($)"),
        "type":   st.column_config.TextColumn("Type"),
        **{c: st.column_config.NumberColumn(c.capitalize()) for c in active_guests},
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

guest_avgs = selected_rows[active_guests].apply(
    pd.to_numeric, errors='coerce'
).mean(skipna=True).round(1)

st.subheader("Average Guest Scores for Selected Whiskeys")
st.table(guest_avgs.rename(index=lambda x: x.capitalize()).to_frame(name="Average Score"))
st.markdown(f"**Overall Average Across All Guests:** `{guest_avgs.mean():.2f}`")

st.markdown("### Your Scores")
user_scores = []
cols = st.columns(3)
for i, (idx, row) in enumerate(selected_rows.iterrows()):
    with cols[i % 3]:
        user_score = st.slider(
            label=f"{row['brand']} — {row['name']}",
            min_value=0.0, max_value=10.0,
            step=0.1, value=5.0, format="%.1f",
            key=f"guest_user_{idx}"
        )
        user_scores.append({"name": row["name"], "Reviewer": "you", "Score": user_score})

box_df = selected_rows.reset_index()[["name"] + active_guests].melt(
    id_vars=["name"], var_name="Reviewer", value_name="Score"
)
box_df = pd.concat([box_df, pd.DataFrame(user_scores)], ignore_index=True)
box_df['Reviewer'] = box_df['Reviewer'].str.capitalize()
box_df['Score']    = pd.to_numeric(box_df['Score'], errors='coerce')

fig = px.box(
    box_df, x="Reviewer", y="Score",
    points="all",
    title="Your Scores vs. the Guests",
    labels={"Score": "Score", "Reviewer": "Reviewer"},
    custom_data=["name"],
    color="Reviewer",
)
fig.update_traces(
    hovertemplate="Reviewer: %{x}<br>Score: %{y}<br>Whiskey: %{customdata[0]}<extra></extra>"
)
fig.update_layout(yaxis_range=[0, 10], showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🎯 Your Closest Guest Match")
user_df_lookup = pd.DataFrame(user_scores).set_index("name")["Score"]
selected_named = selected_rows.set_index("name")

diffs = {}
for r in active_guests:
    col_data    = pd.to_numeric(selected_named[r], errors='coerce').dropna()
    user_common = user_df_lookup.reindex(col_data.index).dropna()
    if not user_common.empty:
        diffs[r.capitalize()] = (col_data.reindex(user_common.index) - user_common).abs().mean()

if diffs:
    closest = min(diffs, key=diffs.get)
    st.success(
        f"Based on your ratings, you align most closely with **{closest}** "
        f"(avg difference: {diffs[closest]:.2f} points)."
    )
    diff_df = pd.DataFrame(
        {"Guest": list(diffs.keys()), "Avg Score Difference": list(diffs.values())}
    ).sort_values("Avg Score Difference")
    st.dataframe(diff_df, hide_index=True, use_container_width=True)