import streamlit as st
import yaml
from pathlib import Path
from utils import add_sidebar_logo

st.set_page_config(
    page_title="Spirited Merch",
    page_icon="🛍️",
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
  /* Link buttons (used for "Buy on ___" links) — match the button styling */
  [data-testid="stLinkButton"] a {
      background: linear-gradient(90deg, #7a3e00, #c8640a) !important;
      color: #fff8ef !important;
      border: none !important;
      border-radius: 8px !important;
      font-family: 'Playfair Display', serif !important;
      font-size: 0.95rem !important;
      padding: 8px 20px !important;
      letter-spacing: 0.5px;
      transition: opacity 0.2s;
      width: 100%;
      justify-content: center;
  }
  [data-testid="stLinkButton"] a:hover { opacity: 0.88 !important; }
  [data-testid="stLinkButton"] a p { color: #fff8ef !important; }
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

  /* ── Merch-specific card styling ──────────────────────────────────────────── */
  .merch-card {
      background: rgba(255,220,160,0.04);
      border: 1px solid rgba(200,100,10,0.25);
      border-radius: 12px;
      padding: 16px;
      height: 100%;
  }
  .merch-price {
      display: inline-block;
      background: rgba(200,100,10,0.18);
      color: #ffd699;
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      padding: 3px 12px;
      border-radius: 20px;
      font-size: 0.95rem;
      margin: 4px 0 8px 0;
  }
  .merch-store {
      color: #d4956a;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
  }
</style>
""", unsafe_allow_html=True)


add_sidebar_logo()

st.title("🛍️ Spirited Merch")
st.caption(
    "Gear for the Spirited crew and fans — tees, drinkware, and more. "
    "Items link out to the store where they're sold."
)

# Uncomment if/when items are actually sold through Amazon affiliate links:
# st.caption("_As an Amazon Associate, Spirited Reviews may earn from qualifying purchases._")

# ── Merch catalog: one file per item ────────────────────────────────────────────
# Items live as individual YAML files in a `merch_items/` folder at the project
# root (a sibling of `pages/` and `utils.py`, NOT inside `pages/`):
#
#   your-project/
#   ├── Spirited_Reviews.py
#   ├── utils.py
#   ├── merch_items/
#   │   ├── logo_tee.yaml
#   │   ├── hoodie.yaml
#   │   └── ...
#   └── pages/
#       └── 9_Spirited_Merch.py
#
# Add an item  → drop a new .yaml file in merch_items/
# Remove an item → delete its .yaml file
# Reorder within a section → set an "order" number in the file (lower = earlier);
#                             items without one sort alphabetically after those that do.
#
# File schema (all fields optional except name/category):
#   name: Spirited Reviews Logo Tee
#   category: Apparel          # must match (or add to) SECTION_ORDER below
#   price: "$25.00"
#   store: Amazon
#   buy_url: ""                # leave blank until you have a real link
#   image_file: Merch_Tee.png  # same lookup as About/Barrel Picks: GitHub repo, then local file
#   description: >
#     Soft cotton tee with the Spirited Reviews logo on the front.
#   order: 1

MERCH_DIR = Path(__file__).resolve().parent.parent / "merch_items"


def load_merch_items():
    items = []
    if not MERCH_DIR.exists():
        return items

    for path in sorted(MERCH_DIR.glob("*.yml")) + sorted(MERCH_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            st.warning(f"Skipping {path.name} — couldn't parse it ({e}).")
            continue

        if not data.get("name"):
            st.warning(f"Skipping {path.name} — missing required 'name' field.")
            continue

        items.append({
            "name": data.get("name"),
            "category": data.get("category", "Other"),
            "price": data.get("price", ""),
            "store": data.get("store", "Store"),
            "buy_url": str(data.get("buy_url") or "").strip(),
            "image_file": data.get("image_file", ""),
            "description": data.get("description", ""),
            "order": data.get("order", 999),
            "_file": path.name,
        })

    items.sort(key=lambda i: (i["order"], i["name"]))
    return items


MERCH_ITEMS = load_merch_items()

# Controls which sections exist and the order they're displayed in.
# To add a new section: add its name here, then set that name as the
# "category" on any item files that belong to it. Any category used in a
# file that ISN'T listed here still shows up (grouped into its own section
# at the end), so nothing silently disappears if you forget to register it.
SECTION_ORDER = ["Apparel", "Glassware", "Supplies"]

# ── Image loader (same pattern as About / Barrel Picks pages) ─────────────────
GITHUB_BASE = "https://github.com/tpfeeney/spirited-reviews/blob/main"


def load_image(filename):
    if not filename or str(filename).strip() in ("", "nan"):
        return None
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


# ── Sidebar: jump to a section ─────────────────────────────────────────────────
# Any category used on an item that isn't in SECTION_ORDER still gets its own
# section, appended after the ones you've explicitly ordered.
extra_categories = sorted(
    {item["category"] for item in MERCH_ITEMS if item["category"] not in SECTION_ORDER}
)
all_sections = SECTION_ORDER + extra_categories

section_option = st.sidebar.radio("Jump to Section:", options=["All"] + all_sections, index=0)

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

sections_to_show = all_sections if section_option == "All" else [section_option]


# ── Product card grid (rendered once per section) ──────────────────────────────
def render_item_grid(items):
    N_COLS = 3
    rows = [items[i:i + N_COLS] for i in range(0, len(items), N_COLS)]

    for row in rows:
        cols = st.columns(N_COLS)
        for col, item in zip(cols, row):
            with col:
                st.markdown('<div class="merch-card">', unsafe_allow_html=True)

                img = load_image(item.get("image_file"))
                if img is not None:
                    st.image(img, use_container_width=True)
                else:
                    st.markdown(
                        "<div style='width:100%;padding:50px 20px;"
                        "background:rgba(255,220,160,0.04);"
                        "border:1px solid rgba(200,100,10,0.2);border-radius:8px;"
                        "text-align:center;color:#7a5a3a;font-size:14px;'>"
                        "🛍️<br>Photo coming soon</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(f"#### {item['name']}")
                st.markdown(
                    f"<span class='merch-price'>{item['price']}</span> "
                    f"<span class='merch-store'>via {item['store']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(item["description"])

                buy_url = item.get("buy_url", "").strip()
                if buy_url.startswith("http"):
                    st.link_button(f"🛒 Buy on {item['store']}", buy_url, use_container_width=True)
                else:
                    st.caption("🔗 Link coming soon")

                st.markdown("</div>", unsafe_allow_html=True)
                st.write("")  # small gap below each card


any_rendered = False
for section in sections_to_show:
    section_items = [item for item in MERCH_ITEMS if item["category"] == section]
    if not section_items:
        continue
    any_rendered = True
    st.header(section)
    render_item_grid(section_items)
    st.markdown("<hr>", unsafe_allow_html=True)

if not any_rendered:
    if not MERCH_ITEMS:
        st.info(
            f"No merch items found. Add `.yaml` files to `{MERCH_DIR.name}/` "
            "at the project root — one file per item — and they'll show up here."
        )
    else:
        st.info("No merch in this section yet — check back soon!")
