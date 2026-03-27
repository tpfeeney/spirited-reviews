import streamlit as st
from utils import add_sidebar_logo

st.set_page_config(
    page_title="Barrel Picks",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

import streamlit as st

# ── Spirited Style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
  h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }

  .stApp {
      background: linear-gradient(135deg, #1a0a00 0%, #2d1400 50%, #1a0a00 100%);
      color: #f5e6d3;
  }
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #120600 0%, #1f0c00 100%) !important;
      border-right: 1px solid rgba(200,100,10,0.25);
  }
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stRadio label,
  [data-testid="stSidebar"] .stCheckbox label {
      color: #f0d5b0 !important;
      font-size: 0.95rem !important;
  }
  [data-testid="stSidebar"] .stMarkdown,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span {
      color: #f0d5b0 !important;
  }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
      color: #ffd699 !important;
  }
  label, .stSelectbox label, .stNumberInput label, .stSlider label,
  .stRadio label, .stCheckbox label, .stMultiSelect label {
      color: #f0d5b0 !important;
      font-size: 0.9rem !important;
  }
  p, li, span, div { color: #f5e6d3; }
  .stNumberInput input, .stTextInput input, .stTextArea textarea {
      background: rgba(255,220,160,0.07) !important;
      border: 1px solid rgba(200,100,10,0.35) !important;
      color: #ffd699 !important;
      border-radius: 6px !important;
  }
  .stSelectbox > div > div, .stMultiSelect > div > div {
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
  /* Metrics */
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, rgba(200,100,10,0.12), rgba(120,60,0,0.18));
      border: 1px solid rgba(200,100,10,0.3);
      border-radius: 10px;
      padding: 12px 16px;
  }
  [data-testid="stMetricLabel"] { color: #d4956a !important; font-size: 0.8rem !important; }
  [data-testid="stMetricValue"] { color: #ffd699 !important; font-family: 'Playfair Display', serif !important; }
  /* Dataframes */
  [data-testid="stDataFrame"] { border: 1px solid rgba(200,100,10,0.2) !important; border-radius: 8px; }
  /* Expander */
  .streamlit-expanderHeader {
      background: rgba(255,220,160,0.06) !important;
      border: 1px solid rgba(200,100,10,0.2) !important;
      border-radius: 8px !important;
      color: #f5a944 !important;
  }
  /* Info / warning / error boxes */
  .stAlert { border-radius: 8px !important; }
  hr { border-color: rgba(200,100,10,0.2) !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


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
        "status": "SOLD OUT",
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
        "status": "SOLD OUT",
        "pick_date": "",
        "release_date": "",
        "image_file": "stogie.jpeg",
        "description": "Aged 72 months in kelvin barrel\nBourbon Fusion:  \n Micro-blend of 4 different barrels - Feb24 (all 21% rye)  \n bbl#1 - Straight bourbon; original barrel date Oct18. \n bbl# 2 - Bourbon finished in Amaro (24 months)  \n bbl# 3 - Bourbon finished in Cognac (15 months)  \n bbl# 4 - Bourbon finished in Apera (15 months)  \n(note: Apera is Australian sherry - similar to PX)",
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
        "status": "SOLD OUT",
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
        "status": "SOLD OUT",
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