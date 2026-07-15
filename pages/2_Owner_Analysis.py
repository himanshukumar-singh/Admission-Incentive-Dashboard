import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Owner Analysis",
    page_icon="👤",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = load_data()

st.title("👤 Owner Performance Analysis")
st.markdown("Analyze individual owner performance across all campuses.")

st.divider()

# ---------------- FILTER ---------------- #

owners = sorted(df["Owner"].unique())

selected_owner = st.selectbox(
    "🔍 Select Owner",
    owners
)

owner_df = df[df["Owner"] == selected_owner]

# ---------------- KPI ---------------- #

total_admission = int(owner_df["TOTAL"].sum())
total_incentive = int(owner_df["Amount"].sum())

campus = owner_df["CAMPUS"].iloc[0]

rank = (
    df.sort_values("Amount", ascending=False)
      .reset_index(drop=True)
)

rank["Rank"] = rank.index + 1

owner_rank = int(rank.loc[rank["Owner"] == selected_owner, "Rank"].iloc[0])

c1, c2, c3, c4 = st.columns(4)

c1.metric("👤 Owner", selected_owner)

c2.metric("🏢 Campus", campus)

c3.metric("🎯 Admissions", total_admission)

c4.metric("💰 Incentive", f"₹ {total_incentive:,.0f}")

st.divider()

# ---------------- RANK ---------------- #

if owner_rank == 1:
    st.success(f"🥇 {selected_owner} is Rank 1 in Incentive Leaderboard!")
elif owner_rank == 2:
    st.info(f"🥈 {selected_owner} is Rank 2 in Incentive Leaderboard!")
elif owner_rank == 3:
    st.info(f"🥉 {selected_owner} is Rank 3 in Incentive Leaderboard!")
else:
    st.warning(f"🏅 Current Rank : {owner_rank}")

st.divider()

# ---------------- CHARTS ---------------- #

left, right = st.columns(2)

with left:

    campus_data = owner_df[
        ["NOIDA", "LUCKNOW", "JAIPUR", "INDORE"]
    ].T.reset_index()

    campus_data.columns = ["Campus", "Admissions"]

    fig = px.bar(
        campus_data,
        x="Campus",
        y="Admissions",
        color="Admissions",
        text="Admissions",
        title="Campus-wise Admissions"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig2 = px.pie(
        values=[total_admission, total_incentive],
        names=["Admissions", "Incentive"],
        hole=.55,
        title="Admissions vs Incentive"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- PERFORMANCE TABLE ---------------- #

st.subheader("📋 Owner Details")

st.dataframe(
    owner_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- COMPARISON ---------------- #

st.subheader("🏆 Top 10 Incentive Earners")

top10 = (
    df.sort_values("Amount", ascending=False)
      .head(10)
)

fig3 = px.bar(
    top10,
    x="Owner",
    y="Amount",
    color="Amount",
    text="Amount",
    title="Top 10 Incentive Earners"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

st.caption("Developed by Himanshu Kumar | Admission Analytics Platform")