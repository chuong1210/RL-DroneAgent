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
from experiments.io_utils import ensure_result_dirs, load_config, model_path, train_log_path, write_csv


TRAINED_ALGOS = {"q_learning", "double_q_learning", "double_q"}


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def epsilon_for_episode(config: dict, episode: int) -> float:
    training = config["training"]
    start = float(training.get("epsilon_start", 1.0))
    end = float(training.get("epsilon_end", 0.02))
    decay = float(training.get("epsilon_decay", 0.9975))
    return max(end, start * (decay ** episode))


def agent_state(env, agent, obs):
    if getattr(agent, "requires_training", False):
        return env.state_encoder(obs)
    return obs


def train_agent(algo: str, wind_mode: str, seed: int, config: dict, output_dir="results", episodes: int | None = None):
    set_seed(seed)
    paths = ensure_result_dirs(output_dir)
    env = DroneDeliveryEnv(wind_mode=wind_mode, config=config, seed=seed)
    agent = create_agent(algo, env, config=config, seed=seed)
    num_episodes = int(episodes or config["training"].get("num_episodes", 3000))
    log_interval = int(config["training"].get("log_interval", 500))
    rows = []

    for episode in range(num_episodes):
        obs, _ = env.reset(seed=seed * 100_000 + episode)
        episode_return = 0.0
        terminated = False
        truncated = False
        epsilon = epsilon_for_episode(config, episode) if getattr(agent, "requires_training", False) else 0.0

        while not (terminated or truncated):
            state_for_agent = agent_state(env, agent, obs)
            action = agent.select_action(state_for_agent, epsilon=epsilon)
            next_obs, reward, terminated, truncated, info = env.step(action)
            next_state_for_agent = agent_state(env, agent, next_obs)
            if getattr(agent, "requires_training", False):
                agent.update(state_for_agent, action, reward, next_state_for_agent, terminated)
            episode_return += reward
            obs = next_obs

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
            "epsilon": epsilon,
        })
        if (episode + 1) % log_interval == 0 or episode == num_episodes - 1:
            recent_rows = rows[-log_interval:]
            avg_return = sum(row["return"] for row in recent_rows) / len(recent_rows)
            success_rate = sum(row["success"] for row in recent_rows) / len(recent_rows)
            avg_steps = sum(row["steps"] for row in recent_rows) / len(recent_rows)
            print(
                f"[{algo}/{wind_mode}/seed={seed}] episode {episode + 1}/{num_episodes} "
                f"epsilon={epsilon:.3f} avg_return={avg_return:.2f} "
                f"success_rate={success_rate:.2%} avg_steps={avg_steps:.1f}"
            )

    write_csv(rows, train_log_path(paths, algo, wind_mode, seed))
    saved_model = None
    if getattr(agent, "requires_training", False):
        saved_model = model_path(paths, algo, wind_mode, seed)
        agent.save(saved_model)
    return {"agent": agent, "model_path": saved_model, "train_log": train_log_path(paths, algo, wind_mode, seed), "rows": rows}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True, choices=["random", "heuristic", "q_learning", "double_q_learning", "double_q"])
    parser.add_argument("--wind-mode", required=True, choices=["observable", "hidden"])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--config", default="experiments/configs.yaml")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--episodes", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)
    result = train_agent(args.algo, args.wind_mode, args.seed, config, output_dir=args.output_dir, episodes=args.episodes)
    print(f"Saved train log: {result['train_log']}")
    if result["model_path"]:
        print(f"Saved model: {result['model_path']}")


if __name__ == "__main__":
    main()
