from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


WIND_FOLDER = {"observable": "wind_obs", "hidden": "wind_hid"}


def copy_demo_models(results_dir="results", seeds=(0, 1, 2)):
    results_dir = Path(results_dir)
    if not results_dir.is_absolute():
        results_dir = PROJECT_ROOT / results_dir
    model_dir = results_dir / "models"
    copied = []
    for wind_mode, folder in WIND_FOLDER.items():
        target_dir = PROJECT_ROOT / "dashboard" / "assets" / "models" / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        for algo, suffix in [("q_learning", ".npy"), ("double_q_learning", ".npz")]:
            for seed in seeds:
                source = model_dir / f"{algo}_{wind_mode}_seed_{seed}{suffix}"
                if source.exists():
                    target = target_dir / f"{algo}_seed{seed}{suffix}"
                    shutil.copy2(source, target)
                    copied.append((source, target))
    return copied


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    return parser.parse_args()


def main():
    args = parse_args()
    copied = copy_demo_models(args.results_dir, tuple(args.seeds))
    for source, target in copied:
        print(f"Copied {source} -> {target}")
    if not copied:
        print("No trained models found to copy.")


if __name__ == "__main__":
    main()
