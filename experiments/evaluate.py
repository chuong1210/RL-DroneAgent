from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.factory import create_agent
from envs import DroneDeliveryEnv
from experiments.io_utils import ensure_result_dirs, eval_log_path, load_config, model_path, summary_path, write_csv, write_json
from experiments.metrics import summarize_episodes


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def agent_state(env, agent, obs):
    if getattr(agent, "requires_training", False):
        return env.state_encoder(obs)
    return obs


def load_agent_model(agent, path):
    if getattr(agent, "requires_training", False):
        if path is None or not Path(path).exists():
            raise FileNotFoundError(f"Model not found: {path}")
        agent.load(path)
    return agent


def evaluate_agent(algo: str, wind_mode: str, seed: int, config: dict, output_dir="results", model=None, episodes: int | None = None):
    set_seed(seed)
    paths = ensure_result_dirs(output_dir)
    env = DroneDeliveryEnv(wind_mode=wind_mode, config=config, seed=seed)
    agent = create_agent(algo, env, config=config, seed=seed + 999)
    selected_model = Path(model) if model else model_path(paths, algo, wind_mode, seed)
    load_agent_model(agent, selected_model)
    num_eval_episodes = int(episodes or config["evaluation"].get("num_eval_episodes", 100))
    rows = []

    for episode in range(num_eval_episodes):
        obs, _ = env.reset(seed=seed * 100_000 + 50_000 + episode)
        episode_return = 0.0
        terminated = False
        truncated = False
        while not (terminated or truncated):
            state_for_agent = agent_state(env, agent, obs)
            action = agent.select_action(state_for_agent, epsilon=0.0)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_return += reward
        rows.append({
            "episode": episode,
            "seed": seed,
            "algo": algo,
            "wind_mode": wind_mode,
            "return": episode_return,
            "steps": info["steps"],
            "success": int(info["success"]),
            "violations": info["violations"],
            "collisions": info["collisions"],
            "pickup_success": int(info["pickup_success"]),
            "dropoff_success": int(info["dropoff_success"]),
        })

    summary = summarize_episodes(rows)
    summary.update({"algo": algo, "wind_mode": wind_mode, "seed": seed, "model_path": str(selected_model) if selected_model else None})
    write_csv(rows, eval_log_path(paths, algo, wind_mode, seed))
    write_json(summary, summary_path(paths, algo, wind_mode, seed))
    return {"summary": summary, "eval_log": eval_log_path(paths, algo, wind_mode, seed), "summary_path": summary_path(paths, algo, wind_mode, seed), "rows": rows}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True, choices=["random", "heuristic", "q_learning", "double_q_learning", "double_q"])
    parser.add_argument("--wind-mode", required=True, choices=["observable", "hidden"])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--config", default="experiments/configs.yaml")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--model", default=None)
    parser.add_argument("--episodes", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)
    result = evaluate_agent(args.algo, args.wind_mode, args.seed, config, output_dir=args.output_dir, model=args.model, episodes=args.episodes)
    print(f"Saved eval log: {result['eval_log']}")
    print(f"Saved summary: {result['summary_path']}")


if __name__ == "__main__":
    main()
