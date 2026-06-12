from __future__ import annotations

import base64
import math
from pathlib import Path

import plotly.graph_objects as go


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DRONE_ICON_PATH = PROJECT_ROOT / "drone.png"

_DRONE_DATA_URI = None


def _drone_image_source():
    """Return a cached data URI for the drone icon so Plotly can render it in the browser."""
    global _DRONE_DATA_URI
    if _DRONE_DATA_URI is None and DRONE_ICON_PATH.exists():
        b64 = base64.b64encode(DRONE_ICON_PATH.read_bytes()).decode()
        _DRONE_DATA_URI = f"data:image/png;base64,{b64}"
    return _DRONE_DATA_URI


CELL = {
    "empty": "#111a28",
    "nofly": "#3a1520",
    "pickup": "#3a2e0d",
    "dropoff": "#0d3324",
    "grid_line": "#243349",
    "path": "#9b6dff",
    "drone_fallback": "#22c7f0",
    "axis": "#8899b4",
}

LABEL_COLORS = {
    "P": "#f0b429",
    "G": "#2ee6a8",
    "✕": "#f2485c",
}


def render_grid_figure(env, title="DRONE FLIGHT", goal_name=""):
    rows, cols = env.config.rows, env.config.cols
    fig = go.Figure()

    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            color = CELL["empty"]
            label = ""
            if pos in env.config.no_fly_zones:
                color = CELL["nofly"]
                label = "✕"
            if pos == env.config.pickup_pos:
                color = CELL["pickup"]
                label = "P"
            if pos == env.config.dropoff_pos:
                color = CELL["dropoff"]
                label = "G"
            fig.add_shape(
                type="rect",
                x0=c - 0.47, x1=c + 0.47,
                y0=r - 0.47, y1=r + 0.47,
                line=dict(color=CELL["grid_line"], width=1.4),
                fillcolor=color,
                layer="below",
            )
            if label:
                fig.add_annotation(
                    x=c, y=r, text=label, showarrow=False,
                    font=dict(size=22, color=LABEL_COLORS.get(label, "#e4ecf5"),
                              family="JetBrains Mono, monospace"),
                )

    if len(env.trajectory) > 1:
        xs = [p[1] for p in env.trajectory]
        ys = [p[0] for p in env.trajectory]
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines+markers",
            line=dict(color=CELL["path"], width=4),
            marker=dict(size=7, color=CELL["path"], line=dict(width=2, color="#0c121c")),
            name="trajectory",
            hoverinfo="skip",
        ))

    r, c = env.position

    # ── HOVER EFFECT ──
    # The drone floats above the cell (y-axis is reversed, so "up" = smaller y)
    # with a gentle bob driven by the step counter, while a soft shadow stays
    # on the ground beneath it — reads as a flying vehicle, not a ground one.
    bob = 0.035 * math.sin(env.steps * 1.1)
    hover_y = r - 0.26 + bob
    shadow_y = r + 0.30
    # shadow shrinks slightly as the drone bobs higher
    shadow_scale = 1.0 - (bob * -2.5)

    for sx, sy, opacity in ((0.30, 0.085, 0.10), (0.22, 0.062, 0.16), (0.14, 0.040, 0.24)):
        sx *= shadow_scale
        sy *= shadow_scale
        fig.add_shape(
            type="circle",
            x0=c - sx, x1=c + sx,
            y0=shadow_y - sy, y1=shadow_y + sy,
            fillcolor=f"rgba(0, 0, 0, {opacity})",
            line=dict(width=0),
            layer="above",
        )

    # faint rotor-wash glow around the hovering drone
    fig.add_shape(
        type="circle",
        x0=c - 0.42, x1=c + 0.42,
        y0=hover_y - 0.42, y1=hover_y + 0.42,
        fillcolor="rgba(34, 199, 240, 0.07)",
        line=dict(color="rgba(34, 199, 240, 0.18)", width=1),
        layer="above",
    )

    drone_src = _drone_image_source()
    if drone_src:
        fig.add_layout_image(dict(
            source=drone_src,
            xref="x", yref="y",
            x=c, y=hover_y,
            sizex=0.85, sizey=0.85,
            xanchor="center", yanchor="middle",
            layer="above",
        ))
    else:
        fig.add_trace(go.Scatter(
            x=[c], y=[hover_y], mode="markers",
            marker=dict(size=44, color=CELL["drone_fallback"],
                        line=dict(color="#e4ecf5", width=3)),
            name="drone",
        ))

    subtitle = f"  ·  GOAL {goal_name}" if goal_name else ""
    fig.update_layout(
        title=dict(
            text=f"{title}{subtitle}", x=0.02,
            font=dict(size=15, color="#e4ecf5", family="JetBrains Mono, monospace"),
        ),
        paper_bgcolor="#0c121c",
        plot_bgcolor="#0c121c",
        height=620,
        margin=dict(l=15, r=15, t=50, b=15),
        showlegend=False,
        xaxis=dict(
            range=[-0.55, cols - 0.45],
            showgrid=False, zeroline=False,
            tickmode="linear", tick0=0, dtick=1,
            color=CELL["axis"], tickfont=dict(size=11),
        ),
        yaxis=dict(
            # extra headroom at the top so the hovering drone is not clipped on row 0
            range=[rows - 0.45, -0.90],
            showgrid=False, zeroline=False,
            tickmode="linear", tick0=0, dtick=1,
            color=CELL["axis"], tickfont=dict(size=11),
            scaleanchor="x", scaleratio=1,
        ),
    )
    return fig
