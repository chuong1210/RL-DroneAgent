from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


PALETTE = {
    "random": "#7f8c8d",
    "heuristic": "#f2c94c",
    "q_learning": "#2f80ed",
    "double_q_learning": "#9b51e0",
    "double_q": "#9b51e0",
}


def setup_style():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "#f6fafb",
        "axes.edgecolor": "#1e2b33",
        "axes.titleweight": "bold",
        "axes.labelcolor": "#10212b",
        "xtick.color": "#10212b",
        "ytick.color": "#10212b",
        "grid.color": "#d3e2e7",
        "font.size": 11,
    })


def moving_average(series, window=50):
    return pd.Series(series).rolling(window=window, min_periods=1).mean()


def plot_learning_curves(results_dir, output_dir, wind_mode="observable", window=50):
    setup_style()
    results_dir = Path(results_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    found = False
    for csv_path in sorted((results_dir / "train").glob(f"*_{wind_mode}_seed_*.csv")):
        df = pd.read_csv(csv_path)
        if df.empty or "episode" not in df:
            continue
        algo = str(df["algo"].iloc[0])
        if int(df["seed"].iloc[0]) != 0:
            continue
        ax.plot(df["episode"], moving_average(df["return"], window), label=algo, color=PALETTE.get(algo), linewidth=2.5)
        found = True
    if not found:
        ax.text(0.5, 0.5, "No training logs found", ha="center", va="center", transform=ax.transAxes)
    ax.set_title(f"Learning curve ({wind_mode}, moving average={window})")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Return")
    ax.grid(True, alpha=0.8)
    ax.legend()
    fig.tight_layout()
    path = output_dir / f"learning_curve_{wind_mode}.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def load_aggregate(results_dir):
    path = Path(results_dir) / "summaries" / "aggregate_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def bar_metric(df, metric, title, ylabel, output_path):
    setup_style()
    fig, ax = plt.subplots(figsize=(11, 5.8))
    if df.empty:
        ax.text(0.5, 0.5, "No aggregate metrics found", ha="center", va="center", transform=ax.transAxes)
    else:
        labels = [f"{a}\n{w}" for a, w in zip(df["algo"], df["wind_mode"])]
        values = df[f"{metric}_mean"]
        errors = df.get(f"{metric}_std", None)
        colors = [PALETTE.get(a, "#2f80ed") for a in df["algo"]]
        ax.bar(labels, values, yerr=errors, color=colors, edgecolor="#10212b", linewidth=1.2, capsize=4)
        if "rate" in metric:
            ax.set_ylim(0, 1.05)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.8)
    fig.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def generate_all_plots(results_dir="results", output_dir="results/figures"):
    results_dir = Path(results_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_aggregate(results_dir)
    paths = []
    paths.append(plot_learning_curves(results_dir, output_dir, "observable"))
    paths.append(plot_learning_curves(results_dir, output_dir, "hidden"))
    paths.append(bar_metric(df, "success_rate", "Success rate comparison", "Success rate", output_dir / "success_rate_comparison.png"))
    paths.append(bar_metric(df, "avg_steps", "Average steps comparison", "Average steps", output_dir / "avg_steps_comparison.png"))
    paths.append(bar_metric(df, "violation_rate", "No-fly violation rate comparison", "Violation rate", output_dir / "violation_rate_comparison.png"))
    paths.append(bar_metric(df[df["algo"].isin(["q_learning", "double_q_learning"])] if not df.empty else df, "success_rate", "Observable vs hidden wind", "Success rate", output_dir / "observable_vs_hidden.png"))
    return paths


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--output-dir", default="results/figures")
    return parser.parse_args()


def main():
    args = parse_args()
    paths = generate_all_plots(args.results_dir, args.output_dir)
    for path in paths:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
