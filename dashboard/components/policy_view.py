from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st


ARROWS = {0: "↑", 1: "→", 2: "↓", 3: "←", 4: "●"}

POLICY_COLORS = {
    "empty": "#0d141e",
    "nofly": "#2d1016",
    "arrow": "#00e5ff",
    "text": "#dce6f0",
    "grid": "#1a2533",
    "nofly_text": "#ff2d55",
}


def q_values(agent):
    if hasattr(agent, "values"):
        return agent.values()
    if hasattr(agent, "q_table"):
        return agent.q_table
    return None


def render_policy_view(agent, env, wind=0, has_package=0):
    values = q_values(agent)
    if values is None:
        st.info("Policy map chỉ hiển thị cho Q-Learning hoặc Double Q-Learning.")
        return

    fig = go.Figure()
    for r in range(env.config.rows):
        for c in range(env.config.cols):
            fill = POLICY_COLORS["empty"]
            text = ""
            text_color = POLICY_COLORS["arrow"]
            if (r, c) in env.config.no_fly_zones:
                fill = POLICY_COLORS["nofly"]
                text = "⛝"
                text_color = POLICY_COLORS["nofly_text"]
            else:
                state = env.state_for_position((r, c), wind=wind, has_package=has_package)
                action = int(np.argmax(values[env.state_encoder(state)]))
                text = ARROWS[action]

            fig.add_shape(
                type="rect",
                x0=c - 0.48, x1=c + 0.48,
                y0=r - 0.48, y1=r + 0.48,
                fillcolor=fill,
                line=dict(color=POLICY_COLORS["grid"], width=1.5),
            )
            fig.add_annotation(
                x=c, y=r, text=text, showarrow=False,
                font=dict(size=22, color=text_color, family="JetBrains Mono, monospace"),
            )

    fig.update_layout(
        title=dict(
            text=f"◆ POLICY MAP  ·  WIND={env.WINDS[wind].upper()}  ·  PKG={'LOADED' if has_package else 'EMPTY'}",
            font=dict(size=14, color="#dce6f0", family="JetBrains Mono, monospace"),
        ),
        paper_bgcolor="#0a1017",
        plot_bgcolor="#0a1017",
        height=560,
        margin=dict(l=20, r=20, t=55, b=20),
        xaxis=dict(
            range=[-0.55, env.config.cols - 0.45],
            showgrid=False, zeroline=False,
            color="#7b8ca3",
        ),
        yaxis=dict(
            range=[env.config.rows - 0.45, -0.55],
            showgrid=False, zeroline=False,
            color="#7b8ca3",
            scaleanchor="x", scaleratio=1,
        ),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
