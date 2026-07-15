import streamlit as st
from utils.data_loader import load_data

st.title("🏆 Leaderboard")

df = load_data()

leaderboard = (
    df.sort_values("Amount", ascending=False)
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

st.subheader("🏆 Incentive Leaderboard")

st.dataframe(
    leaderboard[
        [
            "Position",
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