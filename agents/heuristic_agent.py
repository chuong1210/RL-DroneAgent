import numpy as np

from .base_agent import BaseAgent


class HeuristicAgent(BaseAgent):
    name = "heuristic"
    requires_training = False

    def __init__(self, env, seed=None):
        self.env = env
        self.rng = np.random.default_rng(seed)

    def select_action(self, state, epsilon=0.0):
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.env.num_actions))

        r, c = state[0], state[1]
        has_package = state[-1]
        target = self.env.config.dropoff_pos if has_package else self.env.config.pickup_pos
        candidates = []
        for action, delta in self.env.ACTION_DELTAS.items():
            nr, nc = r + delta[0], c + delta[1]
            pos = (nr, nc)
            if action == 4:
                pos = (r, c)
            invalid = not (0 <= pos[0] < self.env.config.rows and 0 <= pos[1] < self.env.config.cols)
            if invalid or pos in self.env.config.obstacles:
                score = 10_000
            else:
                score = abs(pos[0] - target[0]) + abs(pos[1] - target[1])
                if pos in self.env.config.no_fly_zones:
                    score += 20
                if action == 4:
                    score += 2
            candidates.append((score, action))
        best_score = min(score for score, _ in candidates)
        best_actions = [action for score, action in candidates if score == best_score]
        return int(self.rng.choice(best_actions))
