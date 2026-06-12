import numpy as np

from .base_agent import BaseAgent


class QLearningAgent(BaseAgent):
    name = "q_learning"
    requires_training = True

    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.98, seed=None):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rng = np.random.default_rng(seed)
        self.q_table = np.zeros((num_states, num_actions), dtype=float)

    def select_action(self, state, epsilon=0.0):
        state = int(state)
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.num_actions))
        values = self.q_table[state]
        best = np.flatnonzero(values == values.max())
        return int(self.rng.choice(best))

    def update(self, state, action, reward, next_state, terminated):
        state = int(state)
        next_state = int(next_state)
        old_value = self.q_table[state, action]
        target = reward if terminated else reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state, action] = old_value + self.alpha * (target - old_value)

    def save(self, path):
        np.save(path, self.q_table)

    def load(self, path):
        self.q_table = np.load(path)
        return self

    def values(self):
        return self.q_table
