import streamlit as st
from utils import add_sidebar_logo

add_sidebar_logo()

st.title("🛢️ Barrel Picks")
st.caption("Our hand-selected single barrel picks — past and future.")

# ── Page toggle (right-aligned using columns) ─────────────────────────────────
_, toggle_col = st.columns([3, 1])
with toggle_col:
    view = st.radio("", ["Previous Picks", "Upcoming Picks"], horizontal=False, label_visibility="collapsed")

st.markdown("---")

# ── Data ──────────────────────────────────────────────────────────────────────

previous_picks = [
    {
        "name": "Short Barrel Spirited x Collection",
        "brand": "Shortbarrel Bourbon",
        "date": "",
        "image_file": "shortb.jpg",
        "description": "",
        "proof": "138.2",
        "age": "8 years",
        "location": "Distilled in KY, Aged in Atlanta, Georgia",
        "distillate_info": "OZ Tyler (aka Green River)",
        "pick_team": "Justin and the Collection crew",
        "nose": "",
        "palate": "",
        "mouthfeel": "",
        "finish": "",
    },
    {
        "name": "Backbone Stogiestastic Batch",
        "brand": "",
        "date": "",
        "image_file": "stogie.jpeg",
        "description": "",
        "proof": "",
        "age": "",
        "location": "",
        "distillate_info": "",
        "pick_team": "",
        "nose": "",
        "palate": "",
        "mouthfeel": "",
        "finish": "",
    },
    {
        "name": "Backbone Irish Kelvin",
        "brand": "",
        "date": "",
        "image_file": "irishkelvin.jpg",
        "description": "",
        "proof": "",
        "age": "7.6 years",
        "location": "",
        "distillate_info": "",
        "pick_team": "",
        "nose": "",
        "palate": "",
        "mouthfeel": "",
        "finish": "",
    },
    {
        "name": "Founding Spirit",
        "brand": "",
        "date": "",
        "image_file": "pick_founding_spirit.png",
        "description": "",
        "proof": "",
        "age": "",
        "location": "",
        "distillate_info": "",
        "pick_team": "",
        "nose": "",
        "palate": "",
        "mouthfeel": "",
        "finish": "",
    },
]

upcoming_picks = [
    # {
    #     "name": "Four Roses Single Barrel OBSV",
    #     "brand": "Four Roses",
    #     "date": "Coming Spring 2025",
    #     "image_file": "pick_four_roses.png",
    #     "description": "",
    #     "proof": "",
    #     "age": "",
    #     "location": "",
    #     "distillate_info": "",
    #     "pick_team": "",
    #     "nose": "",
    #     "palate": "",
    #     "mouthfeel": "",
    #     "finish": "",
    # },
]

# ── Image loader ──────────────────────────────────────────────────────────────
GITHUB_BASE = "https://github.com/tpfeeney/spirited-reviews/blob/main"

def load_image(filename):
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
    try:
        return Image.open(filename)
    except Exception:
        return None


# ── Render a single pick card ─────────────────────────────────────────────────
def render_pick(pick):
    st.markdown(f"### {pick['name']}")
    st.caption(f"{pick['brand']}  ·  {pick['date']}")

    img_col, info_col = st.columns([1, 2])

    with img_col:
        img = load_image(pick["image_file"])
        if img is not None:
            st.image(img, use_container_width=True)
        else:
            st.markdown(
                "<div style='width:100%;padding:60px 20px;background:#1a1a1a;"
                "border-radius:8px;text-align:center;color:#888;font-size:14px;'>"
                "🛢️ Photo<br>coming soon</div>",
                unsafe_allow_html=True,
            )

    with info_col:

        # ── Barrel Details ────────────────────────────────────────────────────
        proof          = pick.get("proof", "")
        age            = pick.get("age", "")
        location       = pick.get("location", "")
        distillate_info = pick.get("distillate_info", "")

        if any([proof, age, location, distillate_info]):
            st.markdown("#### 🛢️ Barrel Details")
            detail_cols = st.columns(2)
            with detail_cols[0]:
                if proof:
                    st.markdown(f"**🔢 Proof:** {proof}")
                if age:
                    st.markdown(f"**📅 Age:** {age}")
            with detail_cols[1]:
                if location:
                    st.markdown(f"**📍 Location:** {location}")
                if distillate_info:
                    st.markdown(f"**🌾 Distillate:** {distillate_info}")

        # ── Description ───────────────────────────────────────────────────────
        if pick.get("description"):
            st.markdown("#### 📝 Description")
            st.markdown(pick["description"])

        # ── Pick Team ─────────────────────────────────────────────────────────
        if pick.get("pick_team"):
            st.markdown("#### 👥 Pick Team")
            st.markdown(pick["pick_team"])

        # ── Tasting Notes ─────────────────────────────────────────────────────
        st.markdown("#### 🍶 Tasting Notes")
        tasting_cols = st.columns(2)
        with tasting_cols[0]:
            st.markdown(f"**👃 Nose**  \n{pick.get('nose', '—') or '—'}")
            st.markdown(f"**👄 Palate**  \n{pick.get('palate', '—') or '—'}")
        with tasting_cols[1]:
            st.markdown(f"**💧 Mouthfeel**  \n{pick.get('mouthfeel', '—') or '—'}")
            st.markdown(f"**🔥 Finish**  \n{pick.get('finish', '—') or '—'}")

    st.markdown("---")


# ── Render the selected view ──────────────────────────────────────────────────
if view == "Previous Picks":
    if not previous_picks:
        st.info("No previous picks yet — check back soon!")
    else:
        for pick in previous_picks:
            with st.expander(f"🛢️ {pick['name']}", expanded=False):
                render_pick(pick)

else:
    if not upcoming_picks:
        st.info("No upcoming picks announced yet — stay tuned!")
    else:
        for pick in upcoming_picks:
            render_pick(pick)
