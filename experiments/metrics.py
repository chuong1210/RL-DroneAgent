from __future__ import annotations

from typing import Dict, Iterable, List

import numpy as np
import pandas as pd


METRIC_COLUMNS = [
    "return",
    "steps",
    "success",
    "violations",
    "collisions",
    "pickup_success",
    "dropoff_success",
]


def summarize_episodes(rows: Iterable[dict]) -> Dict[str, float]:
    data = list(rows)
    if not data:
        return {}
    df = pd.DataFrame(data)
    return {
        "num_episodes": int(len(df)),
        "avg_return": float(df["return"].mean()),
        "std_return": float(df["return"].std(ddof=0)),
        "success_rate": float(df["success"].mean()),
        "avg_steps": float(df["steps"].mean()),
        "std_steps": float(df["steps"].std(ddof=0)),
        "violation_rate": float((df["violations"] > 0).mean()),
        "avg_violations": float(df["violations"].mean()),
        "collision_rate": float((df["collisions"] > 0).mean()),
        "avg_collisions": float(df["collisions"].mean()),
        "pickup_rate": float(df["pickup_success"].mean()),
        "dropoff_rate": float(df["dropoff_success"].mean()),
    }


def aggregate_across_seeds(summary_rows: List[dict]) -> pd.DataFrame:
    if not summary_rows:
        return pd.DataFrame()
    df = pd.DataFrame(summary_rows)
    metric_names = [
        "avg_return",
        "success_rate",
        "avg_steps",
        "violation_rate",
        "avg_violations",
        "collision_rate",
        "avg_collisions",
        "pickup_rate",
        "dropoff_rate",
    ]
    output = []
    for (algo, wind_mode), group in df.groupby(["algo", "wind_mode"]):
        row = {"algo": algo, "wind_mode": wind_mode, "num_seeds": int(group["seed"].nunique())}
        for metric in metric_names:
            values = group[metric].to_numpy(dtype=float)
            row[f"{metric}_mean"] = float(np.mean(values))
            row[f"{metric}_std"] = float(np.std(values, ddof=0))
            row[f"{metric}_formatted"] = format_mean_std(row[f"{metric}_mean"], row[f"{metric}_std"], percent="rate" in metric)
        output.append(row)
    return pd.DataFrame(output).sort_values(["wind_mode", "algo"]).reset_index(drop=True)


def format_mean_std(mean: float, std: float, percent: bool = False) -> str:
    if percent:
        return f"{mean * 100:.1f} ± {std * 100:.1f}%"
    return f"{mean:.2f} ± {std:.2f}"
