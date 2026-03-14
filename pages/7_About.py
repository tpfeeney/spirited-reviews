import streamlit as st
import random
import pandas as pd
from utils import add_sidebar_logo, get_data

add_sidebar_logo()

st.title("About the Spirited Crew")
st.write(
    "Welcome to Spirited Reviews, where our goal is honest reviews, bold takes, "
    "and questionable wisdom. Take a look around and see a history of our reviews, "
    "learn about the reviews we've done, and find your spirited palate match. "
    "We hope you enjoy and this helps you stay spirited."
)

# ── Image loader with graceful fallback ───────────────────────────────────────
# Host your images on GitHub (raw URL) or drop the PNGs alongside this file.
# If a file isn't found, a placeholder is shown instead of crashing.
GITHUB_BASE = "https://github.com/tpfeeney/spirited-reviews/blob/main"

def load_image(filename):
    """Try GitHub raw URL first; fall back to local file; return None if both fail."""
    import requests
    from PIL import Image
    from io import BytesIO

    url = f"{GITHUB_BASE}/{filename}?raw=true"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content))
    except Exception:
        pass

    # Local fallback
    try:
        return Image.open(filename)
    except Exception:
        return None


# ── Build live top-5 HTML from data ──────────────────────────────────────────
def top5_html(reviewer_key, df):
    col = pd.to_numeric(df[reviewer_key], errors='coerce')
    top = (
        df.assign(_score=col)
        .dropna(subset=['_score'])
        .sort_values('_score', ascending=False)
        .head(5)[['name', 'brand', '_score']]
    )
    if top.empty:
        return "<div style='font-size:18px;'>No data yet.</div>"
    rows = "".join(
        f"{i+1}) {row['name']} — {row['brand']} "
        f"<span style='color:#c8a84b;font-weight:bold;'>({row['_score']:.1f})</span><br>"
        for i, (_, row) in enumerate(top.iterrows())
    )
    return (
        f"<div style='font-size:18px;'>"
        f"<u><b>Top 5 Reviewed Pours:</b></u><br>{rows}</div>"
    )


# ── Helper to render a person card ───────────────────────────────────────────
def render_person(person, df=None, img_width=None):
    st.markdown(f"#### {person['title']}")
    pic_col, txt_col = st.columns([1, 2])
    with pic_col:
        img = load_image(person["image_file"])
        if img is not None:
            if img_width:
                st.image(img, width=img_width)
            else:
                st.image(img, use_container_width=True)
        else:
            st.markdown(
                "<div style='width:100%;padding:40px;background:#222;"
                "border-radius:8px;text-align:center;color:#888;'>"
                "📷 Photo<br>coming soon</div>",
                unsafe_allow_html=True,
            )
    with txt_col:
        # Bio text
        st.markdown(person["bio"], unsafe_allow_html=True)
        # Live top 5 if reviewer_key provided, otherwise static fallback
        if df is not None and person.get("reviewer_key"):
            st.markdown(top5_html(person["reviewer_key"], df), unsafe_allow_html=True)
        elif person.get("static_top5"):
            st.markdown(person["static_top5"], unsafe_allow_html=True)
        # Bottom line (e.g. favourite spirits)
        if person.get("footer"):
            st.markdown(person["footer"], unsafe_allow_html=True)


# ── Current Crew ──────────────────────────────────────────────────────────────
crew = [
    {
        "title": "Randy (TheDoerofstuff)",
        "image_file": "Randy.png",
        "reviewer_key": "randy",
        "bio": "Randy is awesome, more to come.<br><br>",
        "footer": "<div style='font-size:18px;'><u><b>Top 2 Favorite Spirits:</b></u><br>Still figuring it out</div>",
    },
    {
        "title": "Norm (Mild Turkey)",
        "image_file": "Norm.png",
        "reviewer_key": "norm",
        "bio": """Norm is a dedicated family man who has been married to his wife Ashley for 20 years.
He shares his life with his two wonderful daughters and two semi-loyal girl dogs.
He finds joy in global travel, experiencing new cultures, and is always ready for an outdoor adventure.
When relaxing, he often finds himself savoring a hi-proof scotch or bourbon with a great cigar.<br><br>""",
        "footer": "<div style='font-size:18px;'><u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Scotch</div>",
    },
    {
        "title": "Zach (stat1c_zach)",
        "image_file": "Zach.png",
        "reviewer_key": "zach",
        "bio": """Born in Alabama where the white oak grows tall and strong (or so I've been told).
Auburn University Aerospace Engineer (War Eagle!), now in the Defense Industry.
Competitive curler with 10+ league championships. Bourbon and peated Scotch enthusiast,
aspiring cigar aficionado, and committed foodie with a soft spot for Asian and Italian cuisine.<br><br>""",
        "footer": "<div style='font-size:18px;'><u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Scotch</div>",
    },
]

df = get_data()

random.shuffle(crew)

st.subheader("🥃 The Crew")
# Render first two in a row, then last one solo on the left
cols = st.columns(2)
for i, person in enumerate(crew[:2]):
    with cols[i]:
        render_person(person, df=df)
if len(crew) > 2:
    cols = st.columns(2)
    with cols[0]:
        render_person(crew[2], df=df)

# ── Former Spirited Crew ──────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🏅 Former Spirited Crew")
st.caption("Always a part of the story.")

former = [
    {
        "title": "Justin (Justin)",
        "image_file": "Justin.png",
        "reviewer_key": None,
        "bio": """Collector of old flowers, Four Roses lover, and firm believer that rye whiskey
is proof chaos can be distilled into something beautiful. Proud father of two daughters,
husband of seven years. Finds meaning in good conversation, sharing unique bottles,
and chasing the stories that live between the sips.<br><br>""",
        "static_top5": """<div style='font-size:18px;'><u><b>5 Favorite Pours:</b></u><br>
1) Booker's Rye<br>
2) Watch Hill Proper 20 Batch 2<br>
3) Russell's Reserve 15<br>
4) Parker's Heritage Double Barrel Blend<br>
5) Four Roses Father's Day 2024 16 Year OESV</div>""",
        "footer": "<div style='font-size:18px;'><br><u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Rye</div>",
    },
]

former_cols = st.columns(2)
with former_cols[0]:
    render_person(former[0])