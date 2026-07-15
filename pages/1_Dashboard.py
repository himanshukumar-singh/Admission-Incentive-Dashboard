import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = load_data()

# ---------------- HEADER ---------------- #

st.markdown("""
# 🎓 Admission Analytics Dashboard
### Live Google Sheet Connected 🟢
""")

st.caption(f"Last Refreshed : {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")

st.divider()

# ---------------- KPIs ---------------- #

total_owner = df["Owner"].nunique()
total_admission = int(df["TOTAL"].sum())
total_incentive = int(df["Amount"].sum())

top_row = df.loc[df["Amount"].idxmax()]
top_owner = top_row["Owner"]
top_amount = int(top_row["Amount"])

best_campus = (
    df.groupby("CAMPUS")["TOTAL"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("👥 Owners", total_owner)

c2.metric("🎯 Admissions", total_admission)

c3.metric(
    "💰 Incentive",
    f"₹ {total_incentive:,.0f}"
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

# ---------------- Congratulations ---------------- #

st.success(
    f"🎉 Congratulations **{top_owner}** for achieving the highest incentive of **₹ {top_amount:,.0f}**."
)

st.divider()

# ---------------- Charts ---------------- #

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
        yaxis_title="Amount"
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

# ---------------- Second Row ---------------- #

left, right = st.columns(2)

with left:

    fig3 = px.bar(
        df.sort_values(
            "TOTAL",
            ascending=False
        ),
        x="Owner",
        y="TOTAL",
        color="CAMPUS",
        title="🎯 Owner-wise Admissions"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:

    fig4 = px.scatter(
        df,
        x="TOTAL",
        y="Amount",
        color="CAMPUS",
        size="Amount",
        hover_name="Owner",
        title="📈 Admissions vs Incentive"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# ---------------- Latest Records ---------------- #

st.subheader("📋 Latest Records")

st.dataframe(
    df.sort_values(
        "Amount",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- Footer ---------------- #

st.caption("Developed by Himanshu Kumar | Admission Analytics Platform")