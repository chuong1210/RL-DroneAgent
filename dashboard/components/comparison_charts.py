from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from .learning_curve import ALGO_COLORS, ALGO_NAMES


_LAYOUT = dict(
    paper_bgcolor="#0c121c",
    plot_bgcolor="#0c121c",
    font=dict(color="#8899b4", family="JetBrains Mono, monospace", size=11),
    height=380,
    margin=dict(l=45, r=15, t=55, b=40),
    showlegend=False,
)

_AXIS = dict(
    gridcolor="rgba(100, 160, 220, 0.07)",
    zerolinecolor="rgba(100, 160, 220, 0.14)",
)


def _bar_chart(title, names, values, colors, y_title, errors=None, suffix=""):
    fig = go.Figure(go.Bar(
        x=names, y=values,
        marker=dict(color=colors, line=dict(width=0)),
        error_y=dict(type="data", array=errors, color="#aebdd2", thickness=1.5, width=6) if errors else None,
        text=[f"{v:.1f}{suffix}" for v in values],
        textposition="outside",
        textfont=dict(size=11, color="#e4ecf5", family="JetBrains Mono, monospace"),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#e4ecf5", family="JetBrains Mono, monospace")),
        xaxis=dict(tickfont=dict(size=10), **_AXIS),
        yaxis=dict(title=y_title, **_AXIS),
        **_LAYOUT,
    )
    return fig


def render_comparison_charts(metrics: dict):
    """metrics: {algo: {"success_rate", "avg_steps", "std_steps", "collision_rate"}}"""
    if not metrics:
        st.info("Chưa có dữ liệu đánh giá.")
        return

    algos = list(metrics.keys())
    names = [ALGO_NAMES.get(a, a) for a in algos]
    colors = [ALGO_COLORS.get(a, "#8899b4") for a in algos]

    success = [metrics[a]["success_rate"] * 100 for a in algos]
    steps = [metrics[a]["avg_steps"] for a in algos]
    step_errs = [metrics[a]["std_steps"] for a in algos]
    collisions = [metrics[a]["collision_rate"] * 100 for a in algos]

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.plotly_chart(
            _bar_chart("SUCCESS RATE", names, success, colors, "Tỷ lệ thành công (%)", suffix="%"),
            width="stretch", config={"displayModeBar": False},
        )
    with c2:
        st.plotly_chart(
            _bar_chart("AVG STEPS", names, steps, colors, "Số bước trung bình", errors=step_errs),
            width="stretch", config={"displayModeBar": False},
        )
    with c3:
        st.plotly_chart(
            _bar_chart("COLLISION RATE", names, collisions, colors, "Tỷ lệ va chạm (%)", suffix="%"),
            width="stretch", config={"displayModeBar": False},
        )
