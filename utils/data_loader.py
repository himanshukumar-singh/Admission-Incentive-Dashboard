import pandas as pd
import streamlit as st

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1eziqvaIzCcnkp-VZhgrp15d48N3De_gi4Cks2MYblZg/gviz/tq?tqx=out:csv&sheet=Incentive_Owner"

@st.cache_data(ttl=60)
def load_data():

    df = pd.read_csv(
        GOOGLE_SHEET_URL,
        skiprows=1,
        header=None      # <-- IMPORTANT
    )

    df.columns = [
        "S.No",
        "Owner",
        "CAMPUS",
        "NOIDA",
        "LUCKNOW",
        "JAIPUR",
        "INDORE",
        "TOTAL",
        "Amount"
    ]

    # Header row remove
    df = df[df["S.No"] != "S.No"]

    numeric_cols = [
        "NOIDA",
        "LUCKNOW",
        "JAIPUR",
        "INDORE",
        "TOTAL",
        "Amount"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.reset_index(drop=True)

    return df

# New Google Sheets Link API Connection ================================

# =====================================
# Interview Dashboard Data
# =====================================

# =====================================
# Interview Dashboard Data
# =====================================

INTERVIEW_SHEET_URL = "https://docs.google.com/spreadsheets/d/1fNJX_-CoSK1pn6fSzAeJO8X7DTycRFO_eWTHUGTwEYM/gviz/tq?tqx=out:csv&sheet=DASHBOARD"

@st.cache_data(ttl=60)
def load_interview_data():
    try:
        # Google Sheet Read
        df = pd.read_csv(INTERVIEW_SHEET_URL)

        # Sirf A:E columns (A, B, C, D, E)
        df = df.iloc[:, :5]

        # Blank rows remove
        df = df.dropna(how="all")

        # Column names clean
        df.columns = df.columns.str.strip()

        # Reset Index
        df.reset_index(drop=True, inplace=True)

        return df

    except Exception as e:
        st.error(f"❌ Interview Google Sheet Connection Error: {e}")
        return pd.DataFrame()