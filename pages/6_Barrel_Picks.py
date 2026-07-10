import streamlit as st
import pandas as pd
from utils import add_sidebar_logo

st.set_page_config(
    page_title="Barrel Picks",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, rgba(200,100,10,0.12), rgba(120,60,0,0.18));
      border: 1px solid rgba(200,100,10,0.3);
      border-radius: 10px;
      padding: 12px 16px;
  }
  [data-testid="stMetricLabel"] { color: #d4956a !important; font-size: 0.8rem !important; }
  [data-testid="stMetricValue"] { color: #ffd699 !important; font-family: 'Playfair Display', serif !important; }
  [data-testid="stDataFrame"] { border: 1px solid rgba(200,100,10,0.2) !important; border-radius: 8px; }
  .streamlit-expanderHeader {
      background: rgba(255,220,160,0.06) !important;
      border: 1px solid rgba(200,100,10,0.2) !important;
      border-radius: 8px !important;
      color: #f5a944 !important;
  }
  .stAlert { border-radius: 8px !important; }
  hr { border-color: rgba(200,100,10,0.2) !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

add_sidebar_logo()

st.title("🛢️ Barrel Picks")
st.caption("Our hand-selected single barrel picks — past and future.")

# ── Sheet config ───────────────────────────────────────────────────────────────
SPREADSHEET_ID = "1X4rhHEsj9gWSUfV4SYpuoiaVeEgbecLeqG58XhbeuJE"

# Maps sheet column headers → internal field names used by render_pick()
COLUMN_MAP = {
    "Distillery/Company": "distillery",
    "Brand":              "brand",
    "Distillate":         "distillate_info",
    "Mashbill":           "mashbill",
    "Proof":              "proof",
    "Age":                "age",
    "Pick Name":          "name",
    "Pick Date":          "pick_date",
    "Release Date":       "release_date",
    "Pick Team":          "pick_team",
    "Location":           "location",
    "Nose":               "nose",
    "Palate":             "palate",
    "Mouthfeel":          "mouthfeel",
    "Finish":             "finish",
    "Video":              "video",
    "Status":             "status",
    "Details":            "description",
    "Image File":         "image_file",
    "Image file":         "image_file",
}

# ── Data loader ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_barrel_picks():
    try:
        base = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet="
        dfs = []
        for sheet_name, tab in [("InProg", "upcoming"), ("Released", "previous")]:
            try:
                df = pd.read_csv(base + sheet_name)
                df.columns = df.columns.str.strip()
                df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns}, inplace=True)
                df["_tab"] = tab
                dfs.append(df)
            except Exception:
                pass
        if not dfs:
            st.error("Could not load any barrel picks tabs.")
            return pd.DataFrame()
        combined = pd.concat(dfs, ignore_index=True)
        combined["status"] = combined["status"].astype(str).str.strip().str.lower()
        if "name" in combined.columns:
            combined = combined[combined["name"].astype(str).str.strip().replace("nan", "") != ""]
        return combined
    except Exception as e:
        st.error(f"Could not load barrel picks data: {e}")
        return pd.DataFrame()


# ── Image loader ───────────────────────────────────────────────────────────────
GITHUB_BASE = "https://github.com/tpfeeney/spirited-reviews/blob/main"

def load_image(filename):
    if not filename or str(filename).strip() in ("", "nan"):
        return None
    import requests
    from PIL import Image
    from io import BytesIO

    # Try the filename as-is, then common extension variants
    candidates = [filename]
    if filename.lower().endswith(".jpg"):
        candidates.append(filename[:-4] + ".jpeg")
    elif filename.lower().endswith(".jpeg"):
        candidates.append(filename[:-5] + ".jpg")

    for name in candidates:
        url = f"{GITHUB_BASE}/{name}?raw=true"
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


# ── Helper: clean cell value ───────────────────────────────────────────────────
def cell(pick, key):
    v = str(pick.get(key, "")).strip()
    return "" if v in ("nan", "None", "none") else v


# ── Card renderer ──────────────────────────────────────────────────────────────
def render_pick(pick):
    name       = cell(pick, "name")
    brand      = cell(pick, "brand")
    distillery = cell(pick, "distillery")

    # Brand/Distillery as main title, Pick Name as subtitle
    if brand and distillery and brand.lower() != distillery.lower():
        title = f"{brand} — {distillery}"
    elif brand:
        title = brand
    elif distillery:
        title = distillery
    else:
        title = name  # fallback if no brand/distillery

    st.markdown(f"### {title}")
    if name and name.lower() != title.lower():
      st.markdown(
          f"<p style='font-size:1.1rem; color:#f5a944; font-weight:500; margin-top:-5px;'>"
          f"🥃 {name}</p>",
          unsafe_allow_html=True,
      )
    

    img_col, info_col = st.columns([1, 2])

    with img_col:
        img = load_image(cell(pick, "image_file"))
        if img is not None:
            st.image(img, use_container_width=True)
        else:
            st.markdown(
                "<div style='width:100%;padding:60px 20px;"
                "background:rgba(255,220,160,0.04);"
                "border:1px solid rgba(200,100,10,0.2);border-radius:8px;"
                "text-align:center;color:#7a5a3a;font-size:14px;'>"
                "🛢️<br>Photo coming soon</div>",
                unsafe_allow_html=True,
            )

    with info_col:

        # ── Status / Dates ────────────────────────────────────────────────────
        status       = cell(pick, "status")
        pick_date    = cell(pick, "pick_date")
        release_date = cell(pick, "release_date")
        video        = cell(pick, "video")

        if any([status, pick_date, release_date]):
            st.markdown("#### 📋 Pick Info")
            d1, d2, d3 = st.columns(3)
            with d1:
                if status:
                    color = "#4caf50" if pick.get("_tab") == "upcoming" else "#2196f3"
                    st.markdown(
                        f"**Status:** <span style='color:{color};font-weight:bold;'>"
                        f"{status.title()}</span>",
                        unsafe_allow_html=True,
                    )
            with d2:
                if pick_date:
                    st.markdown(f"**🗓️ Pick Date:** {pick_date}")
            with d3:
                if release_date:
                    st.markdown(f"**🚀 Release Date:** {release_date}")

        # ── Barrel Details ────────────────────────────────────────────────────
        proof           = cell(pick, "proof")
        age             = cell(pick, "age")
        location        = cell(pick, "location")
        distillate_info = cell(pick, "distillate_info")
        mashbill        = cell(pick, "mashbill")

        if any([proof, age, location, distillate_info, mashbill]):
            st.markdown("#### 🛢️ Barrel Details")
            b1, b2 = st.columns(2)
            with b1:
                if proof:        st.markdown(f"**🔢 Proof:** {proof}")
                if age:          st.markdown(f"**📅 Age:** {age}")
                if mashbill:     st.markdown(f"**🌾 Mashbill:** {mashbill}")
            with b2:
                if location:        st.markdown(f"**📍 Location:** {location}")
                if distillate_info: st.markdown(f"**🏭 Distillate:** {distillate_info}")

        # ── Details / Description ─────────────────────────────────────────────
        description = cell(pick, "description")
        if description:
            st.markdown("#### 📝 Details")
            st.markdown(description)

        # ── Pick Team ─────────────────────────────────────────────────────────
        pick_team = cell(pick, "pick_team")
        if pick_team:
            st.markdown("#### 👥 Pick Team")
            st.markdown(pick_team)

        # ── Tasting Notes ─────────────────────────────────────────────────────
        nose      = cell(pick, "nose")
        palate    = cell(pick, "palate")
        mouthfeel = cell(pick, "mouthfeel")
        finish    = cell(pick, "finish")

        if any([nose, palate, mouthfeel, finish]):
            st.markdown("#### 🍶 Tasting Notes")
            t1, t2 = st.columns(2)
            with t1:
                st.markdown(f"**👃 Nose**  \n{nose or '—'}")
                st.markdown(f"**👄 Palate**  \n{palate or '—'}")
            with t2:
                st.markdown(f"**💧 Mouthfeel**  \n{mouthfeel or '—'}")
                st.markdown(f"**🔥 Finish**  \n{finish or '—'}")

        # ── Video link ────────────────────────────────────────────────────────
        if video and video.startswith("http"):
            st.markdown("#### 🎬 Video Review")
            st.markdown(f"[▶ Watch Review]({video})")

    st.markdown("---")


# ── Load & split data ──────────────────────────────────────────────────────────
df_all = load_barrel_picks()

# Split based on which sheet tab the row came from — no hardcoded status values
upcoming_df = df_all[df_all["_tab"] == "upcoming"].copy() if not df_all.empty else pd.DataFrame()
previous_df = df_all[df_all["_tab"] == "previous"].copy() if not df_all.empty else pd.DataFrame()

# ── Sidebar ────────────────────────────────────────────────────────────────────
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ── Page toggle ────────────────────────────────────────────────────────────────
_, toggle_col = st.columns([3, 1])
with toggle_col:
    view = st.radio(
        "", ["Upcoming Picks", "Previous Picks"],
        index=0, horizontal=False, label_visibility="collapsed",
    )

st.markdown("---")

# ── Render ─────────────────────────────────────────────────────────────────────
if view == "Upcoming Picks":
    if upcoming_df.empty:
        st.info("No upcoming picks announced yet — stay tuned!")
    else:
        for _, row in upcoming_df.iterrows():
            render_pick(row.to_dict())

else:
    if previous_df.empty:
        st.info("No previous picks yet — check back soon!")
    else:
        for _, row in previous_df.iterrows():
            with st.expander(f"🛢️ {row.get('name', 'Pick')}", expanded=False):
                render_pick(row.to_dict())