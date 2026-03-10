import streamlit as st
import random
from utils import add_sidebar_logo

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


# ── Helper to render a person card ───────────────────────────────────────────
def render_person(person, img_width=None):
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
        st.markdown(person["text"], unsafe_allow_html=True)


# ── Current Crew ──────────────────────────────────────────────────────────────
crew = [
    {
        "title": "Randy (TheDoerofstuff)",
        "image_file": "Randy.png",
        "text": """Randy is awesome, more to come.

<div style='font-size:18px;'><u><b>5 Favorite Pours:</b></u><br>
1) Malort<br>2) Malort<br>3) Malort<br>4) Malort<br>5) Malort<br><br>
<u><b>Top 2 Favorite Spirits:</b></u><br>Still figuring it out</div>
""",
    },
    {
        "title": "Norm (Mild Turkey)",
        "image_file": "Norm.png",
        "text": """Norm is a dedicated family man who has been married to his wife Ashley for 20 years.
He shares his life with his two wonderful daughters and two semi-loyal girl dogs.
He finds joy in global travel, experiencing new cultures, and is always ready for an outdoor adventure.
When relaxing, he often finds himself savoring a hi-proof scotch or bourbon with a great cigar.

<div style='font-size:18px;'><u><b>5 Favorite Pours:</b></u><br>
1) Parker's Heritage Double Barreled Blend<br>
2) Signatory Vintage Glenallachie 11 yr Speyside Scotch<br>
3) Laphroaig Cairdeas Cask Favorites 10 yr<br>
4) Russell's Reserve Private Single Barrels Picks<br>
5) Rare Character TKO Ryes<br><br>
<u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Scotch</div>
""",
    },
    {
        "title": "Zach (stat1c_zach)",
        "image_file": "Zach.png",
        "text": """Born in Alabama where the white oak grows tall and strong (or so I've been told).
Auburn University Aerospace Engineer (War Eagle!), now in the Defense Industry.
Competitive curler with 10+ league championships. Bourbon and peated Scotch enthusiast,
aspiring cigar aficionado, and committed foodie with a soft spot for Asian and Italian cuisine.

<div style='font-size:18px;'><u><b>5 Favorite Pours:</b></u><br>
1) Parker's Heritage Double Barrel<br>
2) Jack Daniel's 2021 Coy Hill<br>
3) Russell's Reserve 15 Year<br>
4) King of Kentucky 2024<br>
5) Jack Daniel's 14 Year<br><br>
<u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Scotch</div>
""",
    },
]

random.shuffle(crew)

st.subheader("🥃 The Crew")
# Render first two in a row, then last one solo on the left
cols = st.columns(2)
for i, person in enumerate(crew[:2]):
    with cols[i]:
        render_person(person)
if len(crew) > 2:
    cols = st.columns(2)
    with cols[0]:
        render_person(crew[2])

# ── Regular Visitors ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🍶 Regular Visitors")
st.caption("Friends of the show who pull up a chair more often than not.")

visitors = [
    {
        "title": "Tyler Boggs (Boggzilla)",
        "image_file": "boggs.png",
        "text": "<div style='font-size:18px;'>More to come.</div>",
    },
    {
        "title": "Josh (S&W)",
        "image_file": "snw.png",
        "text": "<div style='font-size:18px;'>More to come.</div>",
    },
    {
        "title": "David Mather (Lord Kogac)",
        "image_file": "kogac.png",
        "text": "<div style='font-size:18px;'>More to come.</div>",
    },
]

# Render visitors in rows of 3
visitor_cols = st.columns(3)
for i, person in enumerate(visitors):
    with visitor_cols[i]:
        img_width = 300 if person["image_file"] == "kogac.png" else None
        render_person(person, img_width=img_width)

# ── Former Spirited Crew ──────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🏅 Former Spirited Crew")
st.caption("Always a part of the story.")

former = [
    {
        "title": "Justin (Justin)",
        "image_file": "Justin.png",
        "text": """Collector of old flowers, Four Roses lover, and firm believer that rye whiskey
is proof chaos can be distilled into something beautiful. Proud father of two daughters,
husband of seven years. Finds meaning in good conversation, sharing unique bottles,
and chasing the stories that live between the sips.

<div style='font-size:18px;'><u><b>5 Favorite Pours:</b></u><br>
1) Booker's Rye<br>
2) Watch Hill Proper 20 Batch 2<br>
3) Russell's Reserve 15<br>
4) Parker's Heritage Double Barrel Blend<br>
5) Four Roses Father's Day 2024 16 Year OESV<br><br>
<u><b>Top 2 Favorite Spirits:</b></u><br>Bourbon / Rye</div>
""",
    },
]

former_cols = st.columns(2)
with former_cols[0]:
    render_person(former[0])