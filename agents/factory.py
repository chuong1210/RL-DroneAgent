from .double_q_learning import DoubleQLearningAgent
from .heuristic_agent import HeuristicAgent
from .q_learning import QLearningAgent
from .random_agent import RandomAgent
from .sarsa import SarsaAgent


def create_agent(algo, env, config=None, seed=None):
    config = config or {}
    training = config.get("training", config)
    alpha = float(training.get("alpha", 0.1))
    gamma = float(training.get("gamma", 0.98))
    if algo == "random":
        return RandomAgent(num_actions=env.num_actions, seed=seed)
    if algo == "heuristic":
        return HeuristicAgent(env=env, seed=seed)
    if algo == "q_learning":
        return QLearningAgent(env.num_states, env.num_actions, alpha=alpha, gamma=gamma, seed=seed)
    if algo == "sarsa":
        return SarsaAgent(env.num_states, env.num_actions, alpha=alpha, gamma=gamma, seed=seed)
    if algo in {"double_q", "double_q_learning"}:
        return DoubleQLearningAgent(env.num_states, env.num_actions, alpha=alpha, gamma=gamma, seed=seed)
    raise ValueError(f"Unknown algo: {algo}")
