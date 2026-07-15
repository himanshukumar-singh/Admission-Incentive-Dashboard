import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Admission Analytics Platform",
    page_icon="🎓",
    layout="wide"
)

df = load_data()

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://img.icons8.com/color/96/dashboard-layout.png",
    width=70
)

st.sidebar.title("Admission Analytics")

st.sidebar.success("🟢 Live Google Sheet Connected")

# ---------------- HEADER ----------------

st.markdown("""
# 🎓 Admission Analytics Platform
Live Google Sheet Dashboard
""")

st.divider()

# ---------------- KPIs ----------------

total_owner = df["Owner"].nunique()

total_admission = int(df["TOTAL"].sum())

total_amount = int(df["Amount"].sum())

top_owner = df.loc[df["TOTAL"].idxmax(), "Owner"]

c1,c2,c3,c4 = st.columns(4)

c1.metric("👥 Total Owners", total_owner)

c2.metric("🎯 Admissions", total_admission)

c3.metric("💰 Incentive", f"₹ {total_amount:,.0f}")

c4.metric("🏆 Top Performer", top_owner)

st.divider()

# ---------------- CHARTS ----------------

left,right = st.columns(2)

with left:

    top5 = df.sort_values("TOTAL", ascending=False).head(5)

    fig = px.bar(
        top5,
        x="Owner",
        y="TOTAL",
        title="Top 5 Performers",
        text="TOTAL",
        color="TOTAL"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    campus = df.groupby("CAMPUS")["TOTAL"].sum().reset_index()

    fig2 = px.pie(
        campus,
        names="CAMPUS",
        values="TOTAL",
        hole=.45,
        title="Campus Contribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- LEADERBOARD ----------------

st.subheader("🏆 Leaderboard")

leaderboard = df.sort_values("TOTAL", ascending=False)

st.dataframe(
    leaderboard[
        [
            "Owner",
            "CAMPUS",
            "TOTAL",
            "Amount"
        ]
    ],
    use_container_width=True
)