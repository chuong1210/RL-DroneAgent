from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_config(path="experiments/configs.yaml") -> dict:
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_result_dirs(output_dir="results") -> dict:
    root = Path(output_dir)
    if not root.is_absolute():
        root = PROJECT_ROOT / root
    paths = {
        "root": root,
        "train": root / "train",
        "eval": root / "eval",
        "summaries": root / "summaries",
        "models": root / "models",
        "figures": root / "figures",
        "tables": root / "tables",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def write_csv(rows: Iterable[dict], path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(list(rows)).to_csv(path, index=False)


def write_json(data: dict, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def model_path(paths: dict, algo: str, wind_mode: str, seed: int) -> Path:
    suffix = ".npz" if algo in {"double_q", "double_q_learning"} else ".npy"
    return paths["models"] / f"{algo}_{wind_mode}_seed_{seed}{suffix}"


def train_log_path(paths: dict, algo: str, wind_mode: str, seed: int) -> Path:
    return paths["train"] / f"{algo}_{wind_mode}_seed_{seed}.csv"


def eval_log_path(paths: dict, algo: str, wind_mode: str, seed: int) -> Path:
    return paths["eval"] / f"{algo}_{wind_mode}_seed_{seed}.csv"


def summary_path(paths: dict, algo: str, wind_mode: str, seed: int) -> Path:
    return paths["summaries"] / f"{algo}_{wind_mode}_seed_{seed}.json"
