import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Campus Analysis",
    page_icon="🏢",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = load_data()

st.title("🏢 Campus Performance Analysis")
st.markdown("Campus-wise Admissions & Incentive Analysis")

st.divider()

# ---------------- CAMPUS FILTER ---------------- #

campus_list = sorted(df["CAMPUS"].unique())

selected_campus = st.selectbox(
    "🏢 Select Campus",
    campus_list
)

campus_df = df[df["CAMPUS"] == selected_campus]

# ---------------- KPI ---------------- #

total_owner = campus_df["Owner"].nunique()

total_admission = int(campus_df["TOTAL"].sum())

total_incentive = int(campus_df["Amount"].sum())

top_owner = campus_df.loc[campus_df["Amount"].idxmax(), "Owner"]

top_amount = int(campus_df["Amount"].max())

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Owners",
    total_owner
)

c2.metric(
    "🎯 Admissions",
    total_admission
)

c3.metric(
    "💰 Incentive",
    f"₹ {total_incentive:,.0f}"
)

c4.metric(
    "🏆 Top Performer",
    top_owner,
    f"₹ {top_amount:,.0f}"
)

st.divider()

st.success(
    f"🎉 Congratulations **{top_owner}** for achieving the highest incentive in **{selected_campus} Campus**."
)

st.divider()

# ---------------- CHARTS ---------------- #

left, right = st.columns(2)

with left:

    fig = px.bar(
        campus_df.sort_values("Amount", ascending=False),
        x="Owner",
        y="Amount",
        color="Amount",
        text="Amount",
        title="💰 Owner Wise Incentive"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig2 = px.pie(
        campus_df,
        names="Owner",
        values="TOTAL",
        hole=.50,
        title="🎯 Owner Contribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ---------------- OWNER COMPARISON ---------------- #

st.subheader("📊 Admissions Comparison")

fig3 = px.bar(
    campus_df.sort_values("TOTAL", ascending=False),
    x="Owner",
    y="TOTAL",
    color="TOTAL",
    text="TOTAL"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ---------------- LEADERBOARD ---------------- #

leaderboard = (
    campus_df.sort_values("Amount", ascending=False)
             .reset_index(drop=True)
)

leaderboard.insert(0, "Rank", leaderboard.index + 1)

def medal(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return f"#{rank}"

leaderboard["Position"] = leaderboard["Rank"].apply(medal)

st.subheader("🏆 Campus Leaderboard")

st.dataframe(
    leaderboard[
        [
            "Position",
            "Rank",
            "Owner",
            "TOTAL",
            "Amount"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- DATA TABLE ---------------- #

st.subheader("📋 Campus Data")

st.dataframe(
    campus_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption("Developed by Himanshu Kumar | Admission Analytics Platform")