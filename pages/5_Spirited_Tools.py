import streamlit as st
import pandas as pd
import math
from io import StringIO
from sklearn.linear_model import LinearRegression
from utils import add_sidebar_logo

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spirited Tools",
    page_icon="🥃",
    layout="centered",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
  h1, h2, h3 { font-family: 'Playfair Display', serif; }

  .stApp {
      background: linear-gradient(135deg, #1a0a00 0%, #2d1400 50%, #1a0a00 100%);
      color: #f5e6d3;
  }

  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #120600 0%, #1f0c00 100%) !important;
      border-right: 1px solid rgba(200,100,10,0.25);
  }
  [data-testid="stSidebar"] .stRadio label {
      color: #f0d5b0 !important;
      font-size: 0.97rem !important;
      padding: 4px 0;
  }
  [data-testid="stSidebar"] .stRadio > div { gap: 6px; }

  .sidebar-title {
      font-family: 'Playfair Display', serif;
      color: #ffd699;
      font-size: 1.35rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 4px;
      letter-spacing: 1px;
  }
  .sidebar-sub {
      color: #c9a070;
      font-size: 0.78rem;
      text-align: center;
      margin-bottom: 20px;
      opacity: 0.8;
  }
  .sidebar-divider {
      border: none;
      border-top: 1px solid rgba(200,100,10,0.25);
      margin: 16px 0;
  }
  .header-banner {
      background: linear-gradient(90deg, #7a3e00, #c8640a, #7a3e00);
      border-radius: 12px;
      padding: 24px 32px;
      margin-bottom: 24px;
      text-align: center;
      box-shadow: 0 4px 24px rgba(200, 100, 10, 0.3);
  }
  .header-banner h1 {
      color: #ffd699;
      font-size: 2.2rem;
      margin: 0 0 5px 0;
      letter-spacing: 1px;
  }
  .header-banner p {
      color: #f5dbb5;
      font-size: 0.95rem;
      margin: 0;
      opacity: 0.85;
  }
  .section-card {
      background: rgba(255, 230, 180, 0.06);
      border: 1px solid rgba(200, 100, 10, 0.25);
      border-radius: 10px;
      padding: 20px 22px 12px 22px;
      margin-bottom: 20px;
  }
  .section-title {
      font-family: 'Playfair Display', serif;
      color: #f5a944;
      font-size: 1.05rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 12px;
      padding-bottom: 7px;
      border-bottom: 1px solid rgba(200, 100, 10, 0.2);
  }
  .result-card {
      background: linear-gradient(135deg, rgba(200,100,10,0.15), rgba(120,60,0,0.2));
      border: 1px solid rgba(200,100,10,0.4);
      border-radius: 10px;
      padding: 16px 18px;
      text-align: center;
  }
  .result-card.highlight {
      background: linear-gradient(135deg, rgba(200,100,10,0.35), rgba(160,80,0,0.4));
      border-color: #c8640a;
      box-shadow: 0 2px 16px rgba(200,100,10,0.25);
  }
  .result-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #d4956a;
      margin-bottom: 5px;
  }
  .result-value {
      font-family: 'Playfair Display', serif;
      font-size: 2rem;
      font-weight: 700;
      color: #ffd699;
      line-height: 1;
  }
  .result-sub {
      font-size: 0.8rem;
      color: #c9a070;
      margin-top: 4px;
  }
  .instructions {
      background: rgba(255, 215, 0, 0.08);
      border-left: 3px solid #f5a944;
      border-radius: 0 8px 8px 0;
      padding: 10px 14px;
      margin-bottom: 18px;
      font-size: 0.9rem;
      color: #f5dbb5;
  }
  label, .stSelectbox label, .stNumberInput label, .stSlider label {
      color: #f0d5b0 !important;
      font-size: 0.88rem !important;
  }
  .stNumberInput input, .stTextInput input {
      background: rgba(255,220,160,0.07) !important;
      border: 1px solid rgba(200,100,10,0.35) !important;
      color: #ffd699 !important;
      border-radius: 6px !important;
  }
  .stSelectbox > div > div {
      background: rgba(255,220,160,0.07) !important;
      border: 1px solid rgba(200,100,10,0.35) !important;
      color: #ffd699 !important;
  }
  .stButton > button {
      background: linear-gradient(90deg, #7a3e00, #c8640a) !important;
      color: #fff8ef !important;
      border: none !important;
      border-radius: 8px !important;
      font-family: 'Playfair Display', serif !important;
      font-size: 1rem !important;
      padding: 9px 28px !important;
      letter-spacing: 0.5px;
      transition: opacity 0.2s;
  }
  .stButton > button:hover { opacity: 0.88 !important; }
  hr { border-color: rgba(200,100,10,0.2) !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ─────────────────────────────────────────────────────────
add_sidebar_logo()

with st.sidebar:
    st.markdown('<div class="sidebar-title">🥃 Spirited Tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Bourbon group utilities</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    tool = st.radio(
        "Select a tool",
        options=[
            "🔀 Split Calculator",
            "🌾 Mash Bill Calculator",
            "🔬 Spirited Tools",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#7a5030; font-size:0.75rem; text-align:center;">'
        'Bourbon group utilities v1.0</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# TOOL 1 — Split Calculator
# ══════════════════════════════════════════════════════════════════════════════
if tool == "🔀 Split Calculator":

    st.markdown("""
    <div class="header-banner">
      <h1>🔀 Split Calculator</h1>
      <p>Calculate cost per Facebook spot and per-sample pricing for bourbon group splits</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="instructions">
      📋 <strong>Instructions:</strong> Enter the bottle list on the left, set your options on the right.
      A <strong>bottle split</strong> divides the full bottle volume (and its cost) equally among that many people —
      each person's sample count is drawn from their portion of the bottle.
    </div>
    """, unsafe_allow_html=True)

    def ml_to_oz(ml: float) -> float:
        return ml * 0.033814

    left_col, right_col = st.columns([1.1, 1], gap="large")

    # ── Bottle list ────────────────────────────────────────────────────────────
    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🍾 Bottle List</div>', unsafe_allow_html=True)

        if "bottles" not in st.session_state:
            st.session_state.bottles = [{"name": "", "value": 0.0}]

        def add_bottle():
            st.session_state.bottles.append({"name": "", "value": 0.0})

        def remove_bottle(idx):
            if len(st.session_state.bottles) > 1:
                st.session_state.bottles.pop(idx)

        # Header labels
        h1, h2, _ = st.columns([2.2, 1.5, 0.4])
        h1.markdown("**Bottle Name**")
        h2.markdown("**Value ($)**")

        for i, bottle in enumerate(st.session_state.bottles):
            c1, c2, c3 = st.columns([2.2, 1.5, 0.4])
            with c1:
                st.session_state.bottles[i]["name"] = st.text_input(
                    f"Bottle Name {i+1}",
                    value=bottle["name"],
                    key=f"sc_name_{i}",
                    placeholder="e.g. Old Fitz 10",
                    label_visibility="collapsed",
                )
            with c2:
                raw_val = bottle["value"]
                st.session_state.bottles[i]["value"] = st.number_input(
                    f"Value {i+1} ($)",
                    value=float(raw_val) if raw_val else None,
                    min_value=0.0,
                    step=10.0,
                    key=f"sc_val_{i}",
                    placeholder="0.00",
                    format="%.2f",
                    label_visibility="collapsed",
                )
            with c3:
                st.write("")
                if st.button("✕", key=f"sc_del_{i}", help="Remove bottle"):
                    remove_bottle(i)
                    st.rerun()

        st.button("＋ Add Bottle", on_click=add_bottle, use_container_width=True, key="sc_add")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Options ───────────────────────────────────────────────────────────────
    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Options</div>', unsafe_allow_html=True)

        bottle_size_ml = st.number_input(
            "Bottle Size (mL)", min_value=50.0, max_value=3000.0,
            value=750.0, step=50.0, help="Standard sizes: 375, 700, 750, 1000 mL"
        )
        bottle_size_oz = ml_to_oz(bottle_size_ml)
        st.caption(f"≈ {bottle_size_oz:.2f} fl oz")

        eom_modifier = st.selectbox(
            "W/EOM Modifier", options=["No", "Yes", "No Shipping", "USPS"],
            help="End-of-month modifier affects shipping cost"
        )

        sample_oz = st.selectbox(
            "Sample Size (oz)", options=[0.5, 1.0, 1.5, 2.0], index=1,
            format_func=lambda x: f"{x} oz"
        )

        split_ways = st.selectbox(
            "Bottle Split",
            options=[1, 2, 3, 4, 5],
            index=0,
            format_func=lambda x: "No split" if x == 1 else f"{x}-way split",
            help=(
                "Divide the bottle volume equally among N people. "
                "A 2-way split on a 750 mL bottle gives each person 375 mL "
                "and half the bottle cost."
            )
        )

        # Each person's share
        person_ml = bottle_size_ml / split_ways
        person_oz = bottle_size_oz / split_ways
        if split_ways > 1:
            st.caption(f"Each person's share: **{person_ml:.0f} mL ({person_oz:.2f} oz)**")

        materials_fee = st.checkbox(
            "Add $3.50 materials fee per sample",
            value=False,
            help="Adds $3.50 to the cost of each sample/split to cover materials."
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Calculations ──────────────────────────────────────────────────────────
    num_named        = sum(1 for b in st.session_state.bottles if (b["name"] or "").strip() != "")
    total_value      = sum((b["value"] or 0.0) for b in st.session_state.bottles)
    shipping_map     = {"Yes": 15, "No": 10, "No Shipping": 0, "USPS": 10}
    shipping         = shipping_map[eom_modifier]
    bottle_mult      = 2 if sample_oz >= 1.5 else 1
    num_bottles      = num_named * bottle_mult

    # Split the bottle: each person pays their share of the cost
    # and draws samples from their share of the volume
    value_per_person  = total_value / split_ways
    person_usable_oz  = person_oz - math.fmod(person_oz, sample_oz)
    samp_per_person   = person_usable_oz / sample_oz if sample_oz > 0 else 0

    materials = (3.50 * num_named) if materials_fee else 0.0

    if samp_per_person > 0:
        per_sample_cost = (value_per_person / samp_per_person)  + materials
        fb_spots_auto   = per_sample_cost / 10
    else:
        per_sample_cost = fb_spots_auto = 0

    # ── Whole-number spot suggestions ─────────────────────────────────────────
    # Find all X in 1-200 where total_value % X == 0 (X is a divisor of bottle value).
    # These are the spot counts that give a clean whole-dollar cost per spot.
    whole_dollar_options = {}  # spots -> $/spot
    if total_value > 0:
        for n in range(1, 201):
            if total_value % n == 0:
                whole_dollar_options[n] = int(total_value // n)
    suggestions = sorted(whole_dollar_options.keys())

    # Sample cost card: always based on full bottle (ignores split), shows total samples
    bottle_usable_oz  = bottle_size_oz - math.fmod(bottle_size_oz, sample_oz)
    samp_per_bottle   = bottle_usable_oz / sample_oz if sample_oz > 0 else 0
    total_samples     = int(samp_per_bottle) * num_named
    sample_card_label = f"{sample_oz:.4g} Oz Sample"
    sample_card_sub   = f"{total_samples} sample{'s' if total_samples != 1 else ''} total ({int(samp_per_bottle)} × {num_named} bottle{'s' if num_named != 1 else ''})" if num_named > 0 else f"{int(samp_per_bottle)} samples / bottle"
    # Cost per sample based on full bottle value (no split adjustment)
    if samp_per_bottle > 0 and num_named > 0:
        total_sample_cost = (total_value / samp_per_bottle) + materials
    else:
        total_sample_cost = 0

    # ── FB Spots selector ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="section-title" style="color:#f5a944;font-family:\'Playfair Display\','
        'serif;font-size:1.05rem;font-weight:600;text-transform:uppercase;letter-spacing:2px;'
        'margin-bottom:12px;">\U0001f4ca Results</div>',
        unsafe_allow_html=True
    )

    spots_col, sugg_col = st.columns([1, 2], gap="large")
    with spots_col:
        custom_spots = st.number_input(
            "# of FB Spots",
            min_value=10, max_value=200,
            value=max(10, int(round(fb_spots_auto))),
            step=1,
            help="Choose how many FB spots to run. Cost per spot updates instantly."
        )
    with sugg_col:
        st.markdown(
            '<div style="font-size:0.82rem;color:#d4956a;text-transform:uppercase;'
            'letter-spacing:1.2px;margin-bottom:6px;">💡 Whole-dollar spot counts</div>',
            unsafe_allow_html=True
        )
        if whole_dollar_options:
            # Build labels: "X spots → $Y/spot", sorted by spots ascending
            sugg_labels = [
                f"{n} spots → ${whole_dollar_options[n]}/spot"
                for n in suggestions
            ]
            chosen_sugg = st.radio(
                "Whole-dollar spot counts",
                options=["(use custom)"] + sugg_labels,
                index=0,
                label_visibility="collapsed",
                horizontal=False,
            )
            if chosen_sugg != "(use custom)":
                picked_idx = sugg_labels.index(chosen_sugg)
                custom_spots = suggestions[picked_idx]
        else:
            st.caption("No whole-dollar spot counts exist between 1–200 for this cost.")

    # Final cost using chosen spots
    fb_spots = custom_spots
    cost_per_spot =  total_value / fb_spots if fb_spots > 0 else 0

    value_label = "Each Person Pays" if split_ways > 1 else "Total Value"
    value_sub   = (
        f"of ${total_value:,.0f} total" if split_ways > 1
        else f'{num_named} bottle{"s" if num_named != 1 else ""}'
    )

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(
            f'<div class="result-card"><div class="result-label">{value_label}</div>'
            f'<div class="result-value">${value_per_person:,.0f}</div>'
            f'<div class="result-sub">{value_sub}</div></div>',
            unsafe_allow_html=True
        )
    with r2:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Shipping</div>'
            f'<div class="result-value">${shipping}</div>'
            f'<div class="result-sub">{"No EOM/WOM Modifier" if eom_modifier == "No" else eom_modifier}</div></div>',
            unsafe_allow_html=True
        )
    with r3:
        st.markdown(
            f'<div class="result-card highlight"><div class="result-label">FB Spots</div>'
            f'<div class="result-value">{fb_spots}</div>'
            f'<div class="result-sub">${cost_per_spot:.2f} / spot</div></div>',
            unsafe_allow_html=True
        )
    with r4:
        st.markdown(
            f'<div class="result-card highlight"><div class="result-label">{sample_card_label}</div>'
            f'<div class="result-value">${total_sample_cost:.0f}</div>'
            f'<div class="result-sub">{sample_card_sub}</div></div>',
            unsafe_allow_html=True
        )

    with st.expander("📐 Show Calculation Breakdown", expanded=False):
        st.markdown(f"""
| Input | Value |
|---|---|
| Bottle size | {bottle_size_ml:.0f} mL → {bottle_size_oz:.2f} oz |
| Bottle split | {split_ways}-way → {person_ml:.0f} mL ({person_oz:.2f} oz) per person |
| Usable oz per share (rounded to {sample_oz} oz) | {person_usable_oz:.2f} oz |
| Samples per person's share | {samp_per_person:.0f} |
| Named bottles | {num_named} |
| Bottle count (w/ multiplier) | {num_bottles} |
| Total value | ${total_value:,.2f} |
| Value per person | ${value_per_person:,.2f} |
| Shipping | ${shipping} |
| Materials fee | ${materials:.2f} ($3.50 × {num_named} bottle{'s' if num_named != 1 else ''}) |
| **Cost per sample** | **${per_sample_cost:.2f}** |
| **FB Spots selected** | **{fb_spots}** |
| **Cost per spot** | **${cost_per_spot:.2f}** |
        """)
        st.caption("Formula: (Value per Person ÷ Samples from Share)  = Cost per Sample")
        st.caption("Cost per Spot = Cost per Sample ÷ FB Spots")



# ══════════════════════════════════════════════════════════════════════════════
# TOOL 2 — Mash Bill Calculator
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "🌾 Mash Bill Calculator":

    st.markdown("""
    <div class="header-banner">
      <h1>🌾 Mash Bill Calculator</h1>
      <p>Calculate weighted average grain percentages across blended mash bills</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="instructions">
      📋 <strong>Instructions:</strong> Enter a percentage weight for each grain source per row.
      The weighted average for each grain column is calculated across all rows using the Blend % as the weight.
    </div>
    """, unsafe_allow_html=True)

    STANDARD_GRAINS = ["Corn", "Rye", "Wheat", "Malted Barley", "Malted Rye"]

    if "mash_rows" not in st.session_state:
        st.session_state.mash_rows = [
            {"label": "Mash 1", "pct": None, "grains": {g: None for g in STANDARD_GRAINS}, "custom": []},
            {"label": "Mash 2", "pct": None, "grains": {g: None for g in STANDARD_GRAINS}, "custom": []},
        ]
    if "custom_grain_names" not in st.session_state:
        st.session_state.custom_grain_names = []
    if "_adding_grain" not in st.session_state:
        st.session_state._adding_grain = False

    ctrl_col1, ctrl_col2, _ = st.columns([1.5, 1.8, 4])
    with ctrl_col1:
        if st.button("➕ Add Mash Row"):
            idx = len(st.session_state.mash_rows) + 1
            st.session_state.mash_rows.append({
                "label": f"Mash {idx}", "pct": None,
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
            new_grain_name = st.text_input(
                "New grain name:", key="new_grain_input", placeholder="e.g. Oats, Spelt…"
            )
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
    col_widths = [1.4, 0.8] + [1.0] * len(all_grain_cols) + [0.4]

    header_cols = st.columns(col_widths)
    header_cols[0].markdown("**Mash Label**")
    header_cols[1].markdown("**Blend %**")
    for i, g in enumerate(all_grain_cols):
        header_cols[2 + i].markdown(f"**{g} %**")
    header_cols[-1].markdown("")

    rows_to_delete = []
    for r_idx, row in enumerate(st.session_state.mash_rows):
        row_cols = st.columns(col_widths)
        row["label"] = row_cols[0].text_input(
            "Label", value=row["label"], key=f"mb_label_{r_idx}", label_visibility="collapsed"
        )
        row["pct"] = row_cols[1].number_input(
            "Blend %", min_value=0.0, max_value=100.0, value=row["pct"],
            step=0.1, format="%.1f", key=f"mb_pct_{r_idx}", label_visibility="collapsed",
            placeholder="0.0"
        )
        for g_idx, grain in enumerate(STANDARD_GRAINS):
            row["grains"][grain] = row_cols[2 + g_idx].number_input(
                grain, min_value=0.0, max_value=100.0, value=row["grains"].get(grain),
                step=0.1, format="%.1f", key=f"mb_grain_{r_idx}_{g_idx}",
                label_visibility="collapsed", placeholder="0.0"
            )
        for c_idx, cname in enumerate(st.session_state.custom_grain_names):
            abs_idx = len(STANDARD_GRAINS) + c_idx
            while len(row["custom"]) <= c_idx:
                row["custom"].append(None)
            row["custom"][c_idx] = row_cols[2 + abs_idx].number_input(
                cname, min_value=0.0, max_value=100.0, value=row["custom"][c_idx],
                step=0.1, format="%.1f", key=f"mb_custom_{r_idx}_{c_idx}",
                label_visibility="collapsed", placeholder="0.0"
            )
        if len(st.session_state.mash_rows) > 1:
            if row_cols[-1].button("🗑️", key=f"mb_del_{r_idx}", help="Remove this row"):
                rows_to_delete.append(r_idx)

    for idx in reversed(rows_to_delete):
        st.session_state.mash_rows.pop(idx)
    if rows_to_delete:
        st.rerun()

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


# ══════════════════════════════════════════════════════════════════════════════
# TOOL 3 — Spirited Tools (Alcohol Density Predictor)
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "🔬 Spirited Tools":

    st.markdown("""
    <div class="header-banner">
      <h1>🔬 Spirited Tools</h1>
      <p>Scientific utilities for whiskey analysis and measurement</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("Alcohol Density Predictor")
    st.caption(
        "Enter an alcohol percentage and volume to predict density and mass "
        "at 20°C and 25°C based on published reference data."
    )

    density_data = """percent,20C,25C
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

    ref_df    = pd.read_csv(StringIO(density_data))
    X         = ref_df[['percent']]
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