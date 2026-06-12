from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.evaluate import evaluate_agent
from experiments.io_utils import ensure_result_dirs, load_config
from experiments.metrics import aggregate_across_seeds
from experiments.train import train_agent


def run_sweep(config: dict, output_dir="results", episodes=None, eval_episodes=None):
    paths = ensure_result_dirs(output_dir)
    seeds = config["sweep"].get("seeds", list(range(10)))
    algos = config["sweep"].get("algos", ["random", "heuristic", "q_learning", "double_q_learning"])
    wind_modes = config["sweep"].get("wind_modes", ["observable", "hidden"])
    summaries = []

    for wind_mode in wind_modes:
        for algo in algos:
            for seed in seeds:
                print(f"[train] algo={algo} wind_mode={wind_mode} seed={seed}")
                train_agent(algo, wind_mode, int(seed), config, output_dir=output_dir, episodes=episodes)
                print(f"[eval]  algo={algo} wind_mode={wind_mode} seed={seed}")
                result = evaluate_agent(algo, wind_mode, int(seed), config, output_dir=output_dir, episodes=eval_episodes)
                summaries.append(result["summary"])

    seed_df = pd.DataFrame(summaries)
    seed_csv = paths["summaries"] / "seed_level_metrics.csv"
    seed_df.to_csv(seed_csv, index=False)
    aggregate = aggregate_across_seeds(summaries)
    aggregate_csv = paths["summaries"] / "aggregate_metrics.csv"
    aggregate.to_csv(aggregate_csv, index=False)
    table_csv = paths["tables"] / "aggregate_metrics.csv"
    aggregate.to_csv(table_csv, index=False)
    print(f"Saved seed metrics: {seed_csv}")
    print(f"Saved aggregate metrics: {aggregate_csv}")
    return aggregate


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="experiments/configs.yaml")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--episodes", type=int, default=None)
    parser.add_argument("--eval-episodes", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)
    run_sweep(config, output_dir=args.output_dir, episodes=args.episodes, eval_episodes=args.eval_episodes)


if __name__ == "__main__":
    main()
