import pandas as pd
import streamlit as st

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1eziqvaIzCcnkp-VZhgrp15d48N3De_gi4Cks2MYblZg/gviz/tq?tqx=out:csv&sheet=Incentive_Owner"

@st.cache_data(ttl=60)
def load_data():

    df = pd.read_csv(GOOGLE_SHEET_URL, skiprows=1)

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

    return df