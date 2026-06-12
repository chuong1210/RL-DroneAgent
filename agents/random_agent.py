import numpy as np

from .base_agent import BaseAgent


class RandomAgent(BaseAgent):
    name = "random"
    requires_training = False

    def __init__(self, num_actions=5, seed=None):
        self.num_actions = num_actions
        self.rng = np.random.default_rng(seed)

    def select_action(self, state, epsilon=0.0):
        return int(self.rng.integers(self.num_actions))
