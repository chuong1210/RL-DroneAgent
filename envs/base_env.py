from abc import ABC, abstractmethod


class BaseEnv(ABC):
    @abstractmethod
    def reset(self, seed=None):
        raise NotImplementedError

    @abstractmethod
    def step(self, action):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError

    @abstractmethod
    def state_encoder(self, state):
        raise NotImplementedError

    @abstractmethod
    def state_decoder(self, encoded_state):
        raise NotImplementedError
