import streamlit as st
import pandas as pd
from io import StringIO
from sklearn.linear_model import LinearRegression
from utils import add_sidebar_logo

add_sidebar_logo()

st.title("Spirited Tools 🔬")

# ── Alcohol Density Predictor ─────────────────────────────────────────────────
st.header("Alcohol Density Predictor")
st.caption(
    "Enter an alcohol percentage and volume to predict density and mass "
    "at 20°C and 25°C based on published reference data."
)

data = """percent,20C,25C
40,0.93518,0.93148
41,0.93314,0.92940
42,0.93107,0.92729
43,0.92897,0.92516
44,0.92685,0.92301
45,0.92472,0.92085
46,0.92257,0.91868
47,0.92041,0.91649
48,0.91823,0.91429
49,0.91604,0.91208
50,0.91384,0.90985
51,0.91160,0.90760
52,0.90936,0.90534
53,0.90711,0.90307
54,0.90485,0.90079
55,0.90258,0.89850
56,0.90031,0.89621
57,0.89803,0.89392
58,0.89574,0.89162
59,0.89344,0.88931
60,0.89113,0.88699
61,0.88882,0.88466
62,0.88650,0.88233
63,0.88417,0.87998
64,0.88183,0.87763
65,0.87948,0.87527
66,0.87713,0.87291
67,0.87477,0.87054
68,0.87241,0.86817
69,0.87004,0.86579
70,0.86766,0.86340
71,0.86527,0.86100
72,0.86287,0.85859
73,0.86047,0.85618
74,0.85806,0.85376
75,0.85564,0.85134
76,0.85322,0.84891
77,0.85079,0.84647
78,0.84835,0.84403
79,0.84590,0.84158
80,0.84344,0.83911"""

ref_df = pd.read_csv(StringIO(data))
X = ref_df[['percent']]
model_20C = LinearRegression().fit(X, ref_df['20C'])
model_25C = LinearRegression().fit(X, ref_df['25C'])

col1, col2 = st.columns(2)
with col1:
    percent_input = st.number_input(
        "Alcohol Percent (40–80):", min_value=40.0, max_value=80.0,
        value=None, step=0.1, format="%.2f", placeholder="50.00"
    )
with col2:
    volume_input = st.number_input(
        "Volume (mL):", min_value=0.0, value=None, step=1.0, format="%.2f",
        placeholder="750.00"
    )

# treat None as 0 for the guard check; only compute when both are filled
if percent_input is not None and (volume_input or 0.0) > 0:
    pred_20C = model_20C.predict([[percent_input]])[0]
    pred_25C = model_25C.predict([[percent_input]])[0]
    mass_20C = pred_20C * volume_input
    mass_25C = pred_25C * volume_input

    res1, res2 = st.columns(2)
    with res1:
        st.metric("Density at 20°C", f"{pred_20C:.5f} g/mL")
        st.metric("Mass at 20°C",    f"{mass_20C:.2f} g")
    with res2:
        st.metric("Density at 25°C", f"{pred_25C:.5f} g/mL")
        st.metric("Mass at 25°C",    f"{mass_25C:.2f} g")
else:
    st.info("Enter an alcohol percentage and a volume above 0 mL to see results.")

st.markdown("---")
st.markdown(
    "**Reference:** Osborne et al. *Density and thermal expansion of ethyl alcohol "
    "and of its mixtures with water*. Bulletin of the Bureau of Standards, Vol. 9, "
    "327–474 (1913). [PDF (p. 108)](https://ia800206.us.archive.org/25/items/"
    "dens93274741913197197osbo/dens93274741913197197osbo.pdf#page=108)"
)

st.markdown("---")

# ── Mash Bill Calculator ──────────────────────────────────────────────────────
st.header("Mash Bill Calculator")
st.caption(
    "Enter a percentage weight for each grain source per row. "
    "The weighted average for each grain column is calculated across all rows "
    "using the Blend % as the weight."
)

STANDARD_GRAINS = ["Corn", "Wheat", "Rye", "Malted Barley", "Malted Rye"]

# ── Session state initialisation ──────────────────────────────────────────────
if "mash_rows" not in st.session_state:
    st.session_state.mash_rows = [
        {"label": "Mash 1", "pct": None, "grains": {g: None for g in STANDARD_GRAINS}, "custom": []},
        {"label": "Mash 2", "pct": None, "grains": {g: None for g in STANDARD_GRAINS}, "custom": []},
    ]

if "custom_grain_names" not in st.session_state:
    st.session_state.custom_grain_names = []

if "_adding_grain" not in st.session_state:
    st.session_state._adding_grain = False

# ── Controls: add row / add custom grain column ───────────────────────────────
ctrl_col1, ctrl_col2, _ = st.columns([1.5, 1.8, 4])
with ctrl_col1:
    if st.button("➕ Add Mash Row"):
        idx = len(st.session_state.mash_rows) + 1
        st.session_state.mash_rows.append({
            "label": f"Mash {idx}",
            "pct": None,
            "grains": {g: None for g in STANDARD_GRAINS},
            "custom": [None] * len(st.session_state.custom_grain_names),
        })
        st.rerun()

with ctrl_col2:
    if st.button("➕ Add Grain Column"):
        st.session_state._adding_grain = True

if st.session_state._adding_grain:
    grain_input_col, grain_btn_col = st.columns([3, 1])
    with grain_input_col:
        new_grain_name = st.text_input("New grain name:", key="new_grain_input",
                                        placeholder="e.g. Oats, Spelt…")
    with grain_btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Confirm"):
            name = new_grain_name.strip()
            if name and name not in STANDARD_GRAINS and name not in st.session_state.custom_grain_names:
                st.session_state.custom_grain_names.append(name)
                for row in st.session_state.mash_rows:
                    row["custom"].append(None)
            st.session_state._adding_grain = False
            st.rerun()

all_grain_cols = STANDARD_GRAINS + st.session_state.custom_grain_names

# ── Column layout proportions ─────────────────────────────────────────────────
col_widths = [1.4, 0.8] + [1.0] * len(all_grain_cols) + [0.4]

# ── Header row ────────────────────────────────────────────────────────────────
header_cols = st.columns(col_widths)
header_cols[0].markdown("**Mash Label**")
header_cols[1].markdown("**Blend %**")
for i, g in enumerate(all_grain_cols):
    header_cols[2 + i].markdown(f"**{g} %**")
header_cols[-1].markdown("")

# ── Data rows ─────────────────────────────────────────────────────────────────
rows_to_delete = []

for r_idx, row in enumerate(st.session_state.mash_rows):
    row_cols = st.columns(col_widths)

    row["label"] = row_cols[0].text_input(
        "Label", value=row["label"], key=f"label_{r_idx}", label_visibility="collapsed"
    )
    row["pct"] = row_cols[1].number_input(
        "Blend %", min_value=0.0, max_value=100.0, value=row["pct"],
        step=0.1, format="%.1f", key=f"pct_{r_idx}", label_visibility="collapsed",
        placeholder="0.0"
    )
    for g_idx, grain in enumerate(STANDARD_GRAINS):
        row["grains"][grain] = row_cols[2 + g_idx].number_input(
            grain, min_value=0.0, max_value=100.0,
            value=row["grains"].get(grain),
            step=0.1, format="%.1f", key=f"grain_{r_idx}_{g_idx}", label_visibility="collapsed",
            placeholder="0.0"
        )
    for c_idx, cname in enumerate(st.session_state.custom_grain_names):
        abs_idx = len(STANDARD_GRAINS) + c_idx
        while len(row["custom"]) <= c_idx:
            row["custom"].append(None)
        row["custom"][c_idx] = row_cols[2 + abs_idx].number_input(
            cname, min_value=0.0, max_value=100.0,
            value=row["custom"][c_idx],
            step=0.1, format="%.1f", key=f"custom_{r_idx}_{c_idx}", label_visibility="collapsed",
            placeholder="0.0"
        )
    if len(st.session_state.mash_rows) > 1:
        if row_cols[-1].button("🗑️", key=f"del_{r_idx}", help="Remove this row"):
            rows_to_delete.append(r_idx)

for idx in reversed(rows_to_delete):
    st.session_state.mash_rows.pop(idx)
if rows_to_delete:
    st.rerun()

# ── Weighted output ───────────────────────────────────────────────────────────
st.markdown("#### Weighted Mash Bill")

total_pct = sum((r["pct"] or 0.0) for r in st.session_state.mash_rows)

if total_pct <= 0:
    st.warning("Enter blend percentages that sum to a positive value to see weighted results.")
else:
    if abs(total_pct - 100.0) > 0.05:
        st.warning(
            f"Blend percentages sum to **{total_pct:.1f}%** — "
            "results are normalised to 100% for the weighted calculation."
        )

    weighted = {}
    for grain in all_grain_cols:
        total = 0.0
        for row in st.session_state.mash_rows:
            w = (row["pct"] or 0.0) / total_pct
            if grain in STANDARD_GRAINS:
                val = row["grains"].get(grain) or 0.0
            else:
                c_idx = st.session_state.custom_grain_names.index(grain)
                val = (row["custom"][c_idx] if c_idx < len(row["custom"]) else None) or 0.0
            total += w * val
        weighted[grain] = total

    result_cols = st.columns(len(all_grain_cols))
    for i, grain in enumerate(all_grain_cols):
        result_cols[i].metric(label=grain, value=f"{weighted[grain]:.1f}%")

    with st.expander("Full breakdown table"):
        table_data = []
        for row in st.session_state.mash_rows:
            entry = {"Mash": row["label"], "Blend %": row["pct"] or 0.0}
            for grain in STANDARD_GRAINS:
                entry[grain] = row["grains"].get(grain) or 0.0
            for c_idx, cname in enumerate(st.session_state.custom_grain_names):
                entry[cname] = (row["custom"][c_idx] if c_idx < len(row["custom"]) else None) or 0.0
            table_data.append(entry)
        totals = {"Mash": "Weighted Total", "Blend %": round(total_pct, 1)}
        for grain in all_grain_cols:
            totals[grain] = round(weighted[grain], 1)
        table_data.append(totals)
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)