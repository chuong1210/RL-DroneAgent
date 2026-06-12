from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np

from .base_env import BaseEnv


Position = Tuple[int, int]


@dataclass
class DroneConfig:
    rows: int = 7
    cols: int = 7
    start_pos: Position = (6, 0)
    pickup_pos: Position = (0, 0)
    dropoff_pos: Position = (6, 6)
    no_fly_zones: Tuple[Position, ...] = ((2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4))
    obstacles: Tuple[Position, ...] = ()
    max_steps: int = 120
    wind_push_probability: float = 0.25
    step_penalty: float = -1.0
    wait_penalty: float = -0.5
    collision_penalty: float = -5.0
    no_fly_penalty: float = -20.0
    pickup_reward: float = 10.0
    dropoff_reward: float = 50.0


class DroneDeliveryEnv(BaseEnv):
    ACTIONS: Dict[int, str] = {0: "up", 1: "right", 2: "down", 3: "left", 4: "wait"}
    WINDS: Dict[int, str] = {0: "calm", 1: "north", 2: "east", 3: "west"}
    ACTION_DELTAS: Dict[int, Position] = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1), 4: (0, 0)}
    WIND_DELTAS: Dict[int, Position] = {0: (0, 0), 1: (-1, 0), 2: (0, 1), 3: (0, -1)}

    def __init__(self, wind_mode: str = "observable", config: Optional[dict] = None, seed: Optional[int] = None):
        if wind_mode not in {"observable", "hidden"}:
            raise ValueError("wind_mode must be 'observable' or 'hidden'")
        self.wind_mode = wind_mode
        self.config = self._build_config(config or {})
        self.rng = np.random.default_rng(seed)
        self.num_actions = len(self.ACTIONS)
        self.num_winds = len(self.WINDS)
        self.num_states = self.config.rows * self.config.cols * 2
        if self.wind_mode == "observable":
            self.num_states *= self.num_winds
        self.wind_transition_matrix = self._build_wind_transition_matrix()
        self.reset(seed=seed)

    def _build_config(self, raw: dict) -> DroneConfig:
        env_cfg = raw.get("environment", raw)
        defaults = DroneConfig()
        return DroneConfig(
            rows=int(env_cfg.get("rows", env_cfg.get("grid_rows", env_cfg.get("grid_size", [defaults.rows, defaults.cols])[0]))),
            cols=int(env_cfg.get("cols", env_cfg.get("grid_cols", env_cfg.get("grid_size", [defaults.rows, defaults.cols])[1]))),
            start_pos=tuple(env_cfg.get("start_pos", defaults.start_pos)),
            pickup_pos=tuple(env_cfg.get("pickup_pos", env_cfg.get("pickup_position", defaults.pickup_pos))),
            dropoff_pos=tuple(env_cfg.get("dropoff_pos", env_cfg.get("dropoff_position", defaults.dropoff_pos))),
            no_fly_zones=tuple(tuple(p) for p in env_cfg.get("no_fly_zones", defaults.no_fly_zones)),
            obstacles=tuple(tuple(p) for p in env_cfg.get("obstacles", defaults.obstacles)),
            max_steps=int(env_cfg.get("max_steps", defaults.max_steps)),
            wind_push_probability=float(env_cfg.get("wind_push_probability", defaults.wind_push_probability)),
            step_penalty=float(env_cfg.get("step_penalty", defaults.step_penalty)),
            wait_penalty=float(env_cfg.get("wait_penalty", defaults.wait_penalty)),
            collision_penalty=float(env_cfg.get("collision_penalty", defaults.collision_penalty)),
            no_fly_penalty=float(env_cfg.get("no_fly_penalty", defaults.no_fly_penalty)),
            pickup_reward=float(env_cfg.get("pickup_reward", defaults.pickup_reward)),
            dropoff_reward=float(env_cfg.get("dropoff_reward", defaults.dropoff_reward)),
        )

    def _build_wind_transition_matrix(self) -> np.ndarray:
        matrix = np.full((self.num_winds, self.num_winds), 0.1, dtype=float)
        np.fill_diagonal(matrix, 0.7)
        return matrix

    @property
    def action_space(self) -> List[int]:
        return list(self.ACTIONS.keys())

    @property
    def observation_space_size(self) -> int:
        return self.num_states

    def reset(self, seed: Optional[int] = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.position = self.config.start_pos
        self.wind = int(self.rng.integers(0, self.num_winds))
        self.has_package = 0
        self.steps = 0
        self.cumulative_reward = 0.0
        self.terminated = False
        self.truncated = False
        self.trajectory = [self.position]
        self.last_action = None
        self.last_reward = 0.0
        self.total_violations = 0
        self.total_collisions = 0
        self.pickup_success = False
        self.dropoff_success = False
        return self._get_obs(), self._info()

    def step(self, action: int):
        if action not in self.ACTIONS:
            raise ValueError(f"Invalid action {action}")
        if self.terminated or self.truncated:
            return self._get_obs(), 0.0, self.terminated, self.truncated, self._info()

        self.steps += 1
        previous_position = self.position
        reward = self.config.wait_penalty if action == 4 else self.config.step_penalty
        collision = False
        no_fly_violation = False

        after_action, action_collision = self._move(previous_position, self.ACTION_DELTAS[action])
        if action_collision:
            collision = True

        final_position = after_action
        if self.wind != 0 and self.rng.random() < self.config.wind_push_probability:
            pushed_position, wind_collision = self._move(final_position, self.WIND_DELTAS[self.wind])
            if wind_collision:
                collision = True
            final_position = pushed_position

        self.position = final_position
        if collision:
            reward += self.config.collision_penalty
            self.total_collisions += 1

        if self.position in self.config.no_fly_zones:
            reward += self.config.no_fly_penalty
            no_fly_violation = True
            self.total_violations += 1

        if self.position == self.config.pickup_pos and self.has_package == 0:
            self.has_package = 1
            self.pickup_success = True
            reward += self.config.pickup_reward

        if self.position == self.config.dropoff_pos and self.has_package == 1:
            self.dropoff_success = True
            self.terminated = True
            reward += self.config.dropoff_reward

        if self.steps >= self.config.max_steps and not self.terminated:
            self.truncated = True

        self.cumulative_reward += reward
        self.last_action = action
        self.last_reward = reward
        self.trajectory.append(self.position)
        current_wind = self.wind
        self.wind = int(self.rng.choice(self.num_winds, p=self.wind_transition_matrix[self.wind]))
        info = self._info()
        info.update({"collision": collision, "no_fly_violation": no_fly_violation, "wind_used": current_wind})
        return self._get_obs(), reward, self.terminated, self.truncated, info

    def _move(self, position: Position, delta: Position) -> Tuple[Position, bool]:
        nr = position[0] + delta[0]
        nc = position[1] + delta[1]
        if not (0 <= nr < self.config.rows and 0 <= nc < self.config.cols):
            return position, True
        next_pos = (nr, nc)
        if next_pos in self.config.obstacles:
            return position, True
        return next_pos, False

    def _get_obs(self):
        r, c = self.position
        if self.wind_mode == "observable":
            return (r, c, self.wind, self.has_package)
        return (r, c, self.has_package)

    def _info(self) -> dict:
        return {
            "position": self.position,
            "wind": self.wind,
            "wind_name": self.WINDS[self.wind],
            "has_package": self.has_package,
            "steps": self.steps,
            "cumulative_reward": self.cumulative_reward,
            "last_action": self.last_action,
            "last_action_name": None if self.last_action is None else self.ACTIONS[self.last_action],
            "last_reward": self.last_reward,
            "success": self.dropoff_success,
            "pickup_success": self.pickup_success,
            "dropoff_success": self.dropoff_success,
            "violations": self.total_violations,
            "collisions": self.total_collisions,
            "terminated": self.terminated,
            "truncated": self.truncated,
            "trajectory": list(self.trajectory),
        }

    def state_encoder(self, state) -> int:
        if self.wind_mode == "observable":
            r, c, wind, has_package = state
            return (((int(r) * self.config.cols + int(c)) * self.num_winds + int(wind)) * 2 + int(has_package))
        r, c, has_package = state
        return (int(r) * self.config.cols + int(c)) * 2 + int(has_package)

    def state_decoder(self, encoded_state: int):
        encoded_state = int(encoded_state)
        if self.wind_mode == "observable":
            has_package = encoded_state % 2
            encoded_state //= 2
            wind = encoded_state % self.num_winds
            encoded_state //= self.num_winds
            r = encoded_state // self.config.cols
            c = encoded_state % self.config.cols
            return (r, c, wind, has_package)
        has_package = encoded_state % 2
        encoded_state //= 2
        r = encoded_state // self.config.cols
        c = encoded_state % self.config.cols
        return (r, c, has_package)

    def state_for_position(self, position: Position, wind: int = 0, has_package: int = 0):
        r, c = position
        if self.wind_mode == "observable":
            return (r, c, wind, has_package)
        return (r, c, has_package)

    def render(self):
        symbols = []
        for r in range(self.config.rows):
            row = []
            for c in range(self.config.cols):
                pos = (r, c)
                if pos == self.position:
                    row.append("D")
                elif pos == self.config.pickup_pos:
                    row.append("P")
                elif pos == self.config.dropoff_pos:
                    row.append("G")
                elif pos in self.config.no_fly_zones:
                    row.append("X")
                else:
                    row.append(".")
            symbols.append(" ".join(row))
        return "\n".join(symbols)
