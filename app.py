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
### Live Google Sheet Dashboard
""")

st.divider()

# ---------------- KPIs ----------------

total_owner = df["Owner"].nunique()

total_admission = int(df["TOTAL"].sum())

total_amount = int(df["Amount"].sum())

# Highest Incentive
top_row = df.loc[df["Amount"].idxmax()]

top_owner = top_row["Owner"]

top_amount = int(top_row["Amount"])

best_campus = (
    df.groupby("CAMPUS")["TOTAL"]
      .sum()
      .idxmax()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("👥 Total Owners", total_owner)

c2.metric("🎯 Admissions", total_admission)

c3.metric(
    "💰 Total Incentive",
    f"₹ {total_amount:,.0f}"
)

c4.metric(
    "🏆 Top Performer",
    top_owner,
    f"₹ {top_amount:,.0f}"
)

c5.metric(
    "🏢 Best Campus",
    best_campus
)

st.divider()

st.success(
    f"🎉 Congratulations **{top_owner}** for earning the highest incentive of **₹ {top_amount:,.0f}**."
)

st.divider()

# ---------------- Charts ----------------

left, right = st.columns(2)

with left:

    top5 = (
        df.sort_values(
            "Amount",
            ascending=False
        )
        .head(5)
    )

    fig = px.bar(
        top5,
        x="Owner",
        y="Amount",
        text="Amount",
        color="Amount",
        title="🏆 Top 5 Incentive Earners"
    )

    fig.update_layout(
        xaxis_title="Owner",
        yaxis_title="Incentive"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    campus = (
        df.groupby("CAMPUS")["TOTAL"]
          .sum()
          .reset_index()
    )

    fig2 = px.pie(
        campus,
        names="CAMPUS",
        values="TOTAL",
        hole=.55,
        title="🏢 Campus Contribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ---------------- Leaderboard ----------------

st.subheader("🏆 Incentive Leaderboard")

leaderboard = (
    df.sort_values(
        "Amount",
        ascending=False
    )
    .reset_index(drop=True)
)

leaderboard["Rank"] = leaderboard.index + 1

st.dataframe(
    leaderboard[
        [
            "Rank",
            "Owner",
            "CAMPUS",
            "TOTAL",
            "Amount"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption("Developed by Himanshu Kumar | Admission Analytics Platform")