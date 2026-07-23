import pandas as pd
import streamlit as st
import plotly.express as px
from utils.data_loader import load_interview_data

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Interview Dashboard",
    page_icon="🎯",
    layout="wide"
)

# ==========================================
# Load Data
# ==========================================
df = load_interview_data()

if df.empty:
    st.warning("⚠️ No data found.")
    st.stop()

# ==========================================
# Keep only first 5 columns (A:E)
# ==========================================
df = df.iloc[:, :5].copy()

# Rename Columns
df.columns = [
    "Sr.No",
    "Campus",
    "Owner",
    "CAPI Done",
    "Awaiting CAPI"
]

# Clean Data
df["Campus"] = df["Campus"].astype(str).str.strip()
df["Owner"] = df["Owner"].astype(str).str.strip()

df["CAPI Done"] = pd.to_numeric(
    df["CAPI Done"], errors="coerce"
).fillna(0)

df["Awaiting CAPI"] = pd.to_numeric(
    df["Awaiting CAPI"], errors="coerce"
).fillna(0)

# ==========================================
# Dashboard Title
# ==========================================
st.title("🎯 Interview Dashboard")
st.markdown("### Live Interview Monitoring Dashboard")

# ==========================================
# KPI Cards
# ==========================================
c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Total Owners", df["Owner"].nunique())
c2.metric("🏫 Total Team", df["Campus"].nunique())
c3.metric("✅ Total CAPI Done", int(df["CAPI Done"].sum()))
c4.metric("📌 Awaiting CAPI", int(df["Awaiting CAPI"].sum()))

st.divider()

# ==========================================
# Charts
# ==========================================
left, right = st.columns(2)

# Top 5 Performers
top5 = (
    df.groupby(["Owner", "Campus"], as_index=False)["CAPI Done"]
      .sum()
      .sort_values("CAPI Done", ascending=False)
      .head(5)
)

fig1 = px.bar(
    top5,
    x="Owner",
    y="CAPI Done",
    color="Campus",
    text="CAPI Done",
    title="🏆 Top 5 Performers"
)

left.plotly_chart(fig1, use_container_width=True)

# Campus Wise Performance
campus = (
    df.groupby("Campus", as_index=False)["CAPI Done"]
      .sum()
)

fig2 = px.bar(
    campus,
    x="Campus",
    y="CAPI Done",
    color="Campus",
    text="CAPI Done",
    title="🏫 Campus Wise Performance"
)

right.plotly_chart(fig2, use_container_width=True)

# ==========================================
# Campus Contribution
# ==========================================
fig3 = px.pie(
    campus,
    names="Campus",
    values="CAPI Done",
    hole=0.45,
    title="📊 Campus Wise Contribution"
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# Detail Table
# ==========================================
st.subheader("📋 Owner Wise Details")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)