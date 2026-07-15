import pandas as pd
import streamlit as st

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1eziqvaIzCcnkp-VZhgrp15d48N3De_gi4Cks2MYblZg/gviz/tq?tqx=out:csv&sheet=Incentive_Owner"

@st.cache_data(ttl=60)
def load_data():

    df = pd.read_csv(GOOGLE_SHEET_URL, skiprows=1)

    st.write("RAW DATA")
    st.write(df.head(10))

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

    st.write("RENAMED DATA")
    st.write(df.head(10))

    return df