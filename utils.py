import streamlit as st
import pandas as pd
import numpy as np

# ── Single source of truth for reviewer columns ───────────────────────────────
# Add new reviewers here and every page updates automatically
REVIEWER_COLS = ['randy', 'norm', 'zach', 'justin', 'josh', 'nathan', 'bogzilla', 'chrisj', 'david']


def add_sidebar_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://github.com/tpfeeney/spirited-reviews/blob/main/srlogo.png?raw=true');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                padding-top: 180px;
                background-size: 150px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def score_label(avg):
    """Official Spirited Reviews score labels — aligned with scoring sheet."""
    if pd.isna(avg):
        return np.nan
    elif avg < 4:
        return "Pass"
    elif avg < 5:
        return "Meh"
    elif avg < 6:
        return "Baseline Bottle"
    elif avg < 7:
        return "Weeknight Winner"
    elif avg < 8:
        return "Dependently Delicious"
    elif avg < 9:
        return "Buy-It-Now!"
    else:
        return "One for the Ages!"


@st.cache_data(ttl=3600)
def load_data():
    sheet_id = "1HPjovmE5GFSBUlH-EyZW2ZhteaI22lqqttLrt_ql46k"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    today = pd.Timestamp.today().normalize()
    df = df[df['date'] <= today - pd.Timedelta(days=2)]

    # Only use reviewer cols that actually exist in the sheet
    active_reviewers = [c for c in REVIEWER_COLS if c in df.columns]
    df['avg'] = df[active_reviewers].apply(pd.to_numeric, errors='coerce').mean(axis=1, skipna=True).round(1)
    df['score'] = df['avg'].apply(score_label)

    # Clean age — handles "12 Years", "NAS", "12", bare numbers
    # NAS = Non-Age Stated, a legitimate whiskey term — preserve it
    def clean_age(val):
        if val is None:
            return np.nan
        s = str(val).strip()
        if s.upper() in ('NAS', '', 'NAN', 'NONE', 'N/A'):
            return np.nan
        s = re.sub(r'(?i)\s*years?\s*', '', s).strip()
        try:
            return float(s)
        except ValueError:
            return np.nan
    import re
    df['age'] = df['age'].apply(clean_age)

    # Clean price — handles "$45", "45", "$45.99"
    df['price'] = (
        df['price']
        .astype(str)
        .str.strip()
        .str.replace(r'[\$,]', '', regex=True)
        .replace({'nan': np.nan, '': np.nan})
    )
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # Sort ascending so the most recent entry appears at the bottom of the table
    df = df.sort_values('date', ascending=True).reset_index(drop=True)

    return df


def get_data():
    """Load data into session state if not already present, then return it."""
    if "df" not in st.session_state:
        st.session_state.df = load_data()
    return st.session_state.df