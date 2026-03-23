import streamlit as st
from utils import add_sidebar_logo

add_sidebar_logo()

st.title("🛢️ Barrel Picks")
st.caption("Our hand-selected single barrel picks — past and future.")

# ── Page toggle (right-aligned using columns) ─────────────────────────────────
_, toggle_col = st.columns([3, 1])
with toggle_col:
    view = st.radio("", ["Upcoming Picks", "Previous Picks" ], index=0, horizontal=False, label_visibility="collapsed")

st.markdown("---")

# ── Data ──────────────────────────────────────────────────────────────────────

previous_picks = [
    {
        "name": "Short Barrel Spirited x Collection",
        "brand": "Shortbarrel Bourbon",
        "status": "Released",
        "pick_date": "",
        "release_date": "",
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
        "status": "Released",
        "pick_date": "",
        "release_date": "",
        "image_file": "stogie.jpeg",
        "description": "Aged 72 months in kelvin barrel
Bourbon Fusion:
Micro-blend of 4 different barrels - Feb24 (all 21% rye)
bbl#1 - Straight bourbon; original barrel date Oct18
bbl# 2 - Bourbon finished in Amaro (24 months)
bbl# 3 - Bourbon finished in Cognac (15 months)
bbl# 4 - Bourbon finished in Apera (15 months)
(note: Apera is Australian sherry - similar to PX)",
        "proof": "120",
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
        "status": "Released",
        "pick_date": "",
        "release_date": "",
        "image_file": "irishkelvin.jpg",
        "description": "",
        "proof": "120.9",
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
        "status": "Released",
        "pick_date": "",
        "release_date": "",
        "image_file": "pick_founding_spirit.png",
        "description": "",
        "proof": "",
        "age": "",
        "location": "",
        "distillate_info": "MGP",
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
    #     "status": "Pending Release",   # e.g. "Selected", "In Production", "Pending Release"
    #     "pick_date": "January 2025",
    #     "release_date": "Coming Spring 2025",
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
    {
        "name": "Peerless Rye",
        "brand": "Peerless",
        "status": "Picked",   # e.g. "Selected", "In Production", "Pending Release"
        "pick_date": "Mar 6 2025",
        "release_date": "TBD",
        "image_file": "",
        "description": "",
        "proof": "",
        "age": "",
        "location": "",
        "distillate_info": "",
        "pick_team": "Randy, Norm, Zach, Boggzilla",
        "nose": "",
        "palate": "",
        "mouthfeel": "",
        "finish": "",
    },

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
    st.caption(f"{pick['brand']}")

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

        # ── Status / Dates ────────────────────────────────────────────────────
        status       = pick.get("status", "")
        pick_date    = pick.get("pick_date", "")
        release_date = pick.get("release_date", "")

        if any([status, pick_date, release_date]):
            st.markdown("#### 📋 Pick Info")
            date_cols = st.columns(3)
            with date_cols[0]:
                if status:
                    status_color = (
                        "#4caf50" if status.lower() == "released"
                        else "#ff9800" if "production" in status.lower()
                        else "#2196f3"
                    )
                    st.markdown(
                        f"**Status:** <span style='color:{status_color};font-weight:bold;'>{status}</span>",
                        unsafe_allow_html=True
                    )
            with date_cols[1]:
                if pick_date:
                    st.markdown(f"**🗓️ Pick Date:** {pick_date}")
            with date_cols[2]:
                if release_date:
                    st.markdown(f"**🚀 Release Date:** {release_date}")

        # ── Barrel Details ────────────────────────────────────────────────────
        proof           = pick.get("proof", "")
        age             = pick.get("age", "")
        location        = pick.get("location", "")
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