from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


ALGO_COLORS = {
    "random": "#9aa3b2",
    "heuristic": "#f0b429",
    "q_learning": "#4e9cf5",
    "sarsa": "#2ee6a8",
    "double_q_learning": "#9b6dff",
}

ALGO_NAMES = {
    "random": "Random",
    "heuristic": "Heuristic",
    "q_learning": "Q-Learning",
    "sarsa": "SARSA",
    "double_q_learning": "Double Q-Learning",
}

_LAYOUT = dict(
    paper_bgcolor="#0c121c",
    plot_bgcolor="#0c121c",
    font=dict(color="#8899b4", family="JetBrains Mono, monospace", size=11),
    height=430,
    margin=dict(l=50, r=20, t=55, b=45),
    legend=dict(
        bgcolor="rgba(12, 18, 28, 0.9)",
        bordercolor="rgba(100, 160, 220, 0.15)",
        borderwidth=1,
        font=dict(size=11, color="#aebdd2"),
        orientation="h",
        yanchor="bottom", y=1.02, xanchor="left", x=0,
    ),
)

_AXIS = dict(
    gridcolor="rgba(100, 160, 220, 0.07)",
    zerolinecolor="rgba(100, 160, 220, 0.14)",
    title_font=dict(size=11),
)


def render_learning_curves(curves: dict, window: int = 100, target_pct: float = 85.0):
    """curves: {algo: DataFrame(episode, return, success)} — renders the reward
    and success-rate charts side by side."""
    if not curves:
        st.info("Chưa có dữ liệu huấn luyện.")
        return

    reward_fig = go.Figure()
    success_fig = go.Figure()

    max_ep = 0
    for algo, df in curves.items():
        if df is None or df.empty:
            continue
        color = ALGO_COLORS.get(algo, "#8899b4")
        name = ALGO_NAMES.get(algo, algo)
        max_ep = max(max_ep, int(df["episode"].max()))

        reward_ma = df["return"].rolling(window=window, min_periods=1).mean()
        reward_fig.add_trace(go.Scatter(
            x=df["episode"], y=reward_ma, mode="lines", name=name,
            line=dict(width=2.4, color=color),
        ))

        success_ma = df["success"].rolling(window=window, min_periods=1).mean() * 100
        success_fig.add_trace(go.Scatter(
            x=df["episode"], y=success_ma, mode="lines", name=name,
            line=dict(width=2.4, color=color),
        ))

    reward_fig.update_layout(
        title=dict(text=f"REWARD QUA CÁC EPISODE (MA {window})",
                   font=dict(size=13, color="#e4ecf5", family="JetBrains Mono, monospace")),
        xaxis=dict(title="Episode", **_AXIS),
        yaxis=dict(title="Reward (trung bình trượt)", **_AXIS),
        **_LAYOUT,
    )

    success_fig.add_shape(
        type="line", x0=0, x1=max(max_ep, 1), y0=target_pct, y1=target_pct,
        line=dict(color="#f2485c", width=2, dash="dash"),
    )
    success_fig.add_annotation(
        x=max(max_ep, 1), y=target_pct, text=f"Target {target_pct:.0f}%",
        showarrow=False, xanchor="right", yanchor="bottom",
        font=dict(size=11, color="#f2485c", family="JetBrains Mono, monospace"),
    )
    success_fig.update_layout(
        title=dict(text=f"SUCCESS RATE (%) (MA {window})",
                   font=dict(size=13, color="#e4ecf5", family="JetBrains Mono, monospace")),
        xaxis=dict(title="Episode", **_AXIS),
        yaxis=dict(title="Tỷ lệ thành công (%)", range=[-5, 105], **_AXIS),
        **_LAYOUT,
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(reward_fig, width="stretch", config={"displayModeBar": False})
    with c2:
        st.plotly_chart(success_fig, width="stretch", config={"displayModeBar": False})
