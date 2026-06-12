from __future__ import annotations

from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "background": "#eef4f7",
    "grid": "#26343c",
    "drone": "#2f80ed",
    "pickup": "#f2c94c",
    "dropoff": "#27ae60",
    "nofly": "#eb5757",
    "trajectory": "#9b51e0",
    "text": "#10212b",
}


def render_grid(env, trajectory: Optional[Iterable[tuple]] = None, title: str = "Drone delivery in wind"):
    rows, cols = env.config.rows, env.config.cols
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_facecolor(COLORS["background"])
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color=COLORS["grid"], linewidth=1.2, alpha=0.65)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.tick_params(length=0, labelsize=9)

    for r, c in env.config.no_fly_zones:
        ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color=COLORS["nofly"], alpha=0.82))
        ax.text(c, r, "NO", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    pr, pc = env.config.pickup_pos
    dr, dc = env.config.dropoff_pos
    ax.scatter([pc], [pr], s=720, marker="s", c=COLORS["pickup"], edgecolors="#332900", linewidths=2, zorder=4)
    ax.text(pc, pr, "P", ha="center", va="center", fontsize=18, fontweight="bold", color="#332900")
    ax.scatter([dc], [dr], s=720, marker="s", c=COLORS["dropoff"], edgecolors="#083b1d", linewidths=2, zorder=4)
    ax.text(dc, dr, "D", ha="center", va="center", fontsize=18, fontweight="bold", color="white")

    path = list(trajectory or env.trajectory)
    if len(path) > 1:
        ys = [p[0] for p in path]
        xs = [p[1] for p in path]
        ax.plot(xs, ys, color=COLORS["trajectory"], linewidth=4, alpha=0.65, zorder=3)
        ax.scatter(xs[:-1], ys[:-1], s=34, color=COLORS["trajectory"], alpha=0.45, zorder=3)

    r, c = env.position
    ax.scatter([c], [r], s=900, marker="o", c=COLORS["drone"], edgecolors="white", linewidths=3, zorder=6)
    ax.text(c, r, "✦", ha="center", va="center", fontsize=22, color="white", fontweight="bold", zorder=7)
    wind_arrow = {"calm": "•", "north": "↑", "east": "→", "west": "←"}[env.WINDS[env.wind]]
    ax.set_title(f"{title}   Wind: {env.WINDS[env.wind]} {wind_arrow}", fontsize=14, fontweight="bold", color=COLORS["text"], pad=14)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    return fig
