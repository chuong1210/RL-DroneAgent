from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


ARROWS = {0: "↑", 1: "→", 2: "↓", 3: "←", 4: "•"}


def agent_q_values(agent):
    if hasattr(agent, "values"):
        return agent.values()
    if hasattr(agent, "q_table"):
        return agent.q_table
    return None


def plot_policy_arrows(agent, env, wind=0, has_package=0, title=None, save_path=None):
    q_values = agent_q_values(agent)
    if q_values is None:
        raise ValueError("Policy arrows require a tabular RL agent")

    rows, cols = env.config.rows, env.config.cols
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="#23313a", linewidth=1.2, alpha=0.7)
    ax.set_xticks([])
    ax.set_yticks([])

    for r, c in env.config.no_fly_zones:
        ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color="#eb5757", alpha=0.75))

    for r in range(rows):
        for c in range(cols):
            if (r, c) in env.config.no_fly_zones:
                continue
            state = env.state_for_position((r, c), wind=wind, has_package=has_package)
            encoded = env.state_encoder(state)
            action = int(np.argmax(q_values[encoded]))
            ax.text(c, r, ARROWS[action], ha="center", va="center", fontsize=24, fontweight="bold", color="#10212b")

    pr, pc = env.config.pickup_pos
    dr, dc = env.config.dropoff_pos
    ax.text(pc, pr, "P", ha="center", va="center", fontsize=13, fontweight="bold", color="#8a6d00")
    ax.text(dc, dr, "D", ha="center", va="center", fontsize=13, fontweight="bold", color="#146b35")
    ax.set_title(title or f"Policy arrows | wind={env.WINDS[wind]} | has_package={has_package}", fontsize=13, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_value_heatmap(agent, env, wind=0, has_package=0, title=None, save_path=None):
    q_values = agent_q_values(agent)
    if q_values is None:
        raise ValueError("Value heatmap requires a tabular RL agent")
    values = np.zeros((env.config.rows, env.config.cols))
    for r in range(env.config.rows):
        for c in range(env.config.cols):
            state = env.state_for_position((r, c), wind=wind, has_package=has_package)
            values[r, c] = float(np.max(q_values[env.state_encoder(state)]))
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(values, cmap="viridis")
    for r, c in env.config.no_fly_zones:
        ax.text(c, r, "X", ha="center", va="center", color="white", fontsize=16, fontweight="bold")
    ax.set_title(title or f"State value heatmap | wind={env.WINDS[wind]} | has_package={has_package}", fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig
