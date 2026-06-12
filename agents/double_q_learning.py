import numpy as np

from .base_agent import BaseAgent


class DoubleQLearningAgent(BaseAgent):
    name = "double_q_learning"
    requires_training = True

    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.98, seed=None):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rng = np.random.default_rng(seed)
        self.q1 = np.zeros((num_states, num_actions), dtype=float)
        self.q2 = np.zeros((num_states, num_actions), dtype=float)

    def select_action(self, state, epsilon=0.0):
        state = int(state)
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.num_actions))
        values = self.q1[state] + self.q2[state]
        best = np.flatnonzero(values == values.max())
        return int(self.rng.choice(best))

    def update(self, state, action, reward, next_state, terminated):
        state = int(state)
        next_state = int(next_state)
        if self.rng.random() < 0.5:
            old_value = self.q1[state, action]
            if terminated:
                target = reward
            else:
                best_next = int(np.argmax(self.q1[next_state]))
                target = reward + self.gamma * self.q2[next_state, best_next]
            self.q1[state, action] = old_value + self.alpha * (target - old_value)
        else:
            old_value = self.q2[state, action]
            if terminated:
                target = reward
            else:
                best_next = int(np.argmax(self.q2[next_state]))
                target = reward + self.gamma * self.q1[next_state, best_next]
            self.q2[state, action] = old_value + self.alpha * (target - old_value)

    def save(self, path):
        np.savez(path, q1=self.q1, q2=self.q2)

    def load(self, path):
        data = np.load(path)
        if isinstance(data, np.lib.npyio.NpzFile):
            self.q1 = data["q1"]
            self.q2 = data["q2"]
        else:
            self.q1 = data
            self.q2 = np.zeros_like(data)
        return self

    def values(self):
        return self.q1 + self.q2
