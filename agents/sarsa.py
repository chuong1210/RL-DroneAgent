import numpy as np

from .base_agent import BaseAgent


class SarsaAgent(BaseAgent):
    """On-policy SARSA. update() samples the next action a' with the current
    epsilon and stores it; the following select_action() returns that stored
    action so the TD target Q(s', a') matches the action actually taken."""

    name = "sarsa"
    requires_training = True

    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.98, seed=None):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rng = np.random.default_rng(seed)
        self.q_table = np.zeros((num_states, num_actions), dtype=float)
        self._epsilon = 0.0
        self._pending_action = None
        self._pending_state = None
        self._pending_epsilon = None

    def _egreedy(self, state, epsilon):
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.num_actions))
        values = self.q_table[int(state)]
        best = np.flatnonzero(values == values.max())
        return int(self.rng.choice(best))

    def select_action(self, state, epsilon=0.0):
        self._epsilon = epsilon
        state = int(state)
        # Replay the pending action only within the same episode: the state and
        # the epsilon it was sampled with must both match, otherwise a stale
        # action from a truncated episode could leak into the next one (or into
        # greedy evaluation with epsilon = 0).
        if (
            self._pending_action is not None
            and self._pending_state == state
            and self._pending_epsilon == epsilon
        ):
            action = self._pending_action
            self._pending_action = None
            return action
        self._pending_action = None
        return self._egreedy(state, epsilon)

    def update(self, state, action, reward, next_state, terminated):
        state = int(state)
        next_state = int(next_state)
        if terminated:
            target = reward
            self._pending_action = None
        else:
            next_action = self._egreedy(next_state, self._epsilon)
            target = reward + self.gamma * self.q_table[next_state, next_action]
            self._pending_action = next_action
            self._pending_state = next_state
            self._pending_epsilon = self._epsilon
        old_value = self.q_table[state, action]
        self.q_table[state, action] = old_value + self.alpha * (target - old_value)

    def save(self, path):
        np.save(path, self.q_table)

    def load(self, path):
        self.q_table = np.load(path)
        return self

    def values(self):
        return self.q_table
