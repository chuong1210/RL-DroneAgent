from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name = "base"
    requires_training = False

    @abstractmethod
    def select_action(self, state, epsilon=0.0):
        raise NotImplementedError

    def update(self, state, action, reward, next_state, terminated):
        return None

    def save(self, path):
        return None

    def load(self, path):
        return self
