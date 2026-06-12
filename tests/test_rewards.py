from envs import DroneDeliveryEnv


def build_env():
    config = {
        "environment": {
            "start_pos": [6, 0],
            "pickup_pos": [0, 0],
            "dropoff_pos": [6, 6],
            "no_fly_zones": [[2, 2]],
            "obstacles": [],
            "max_steps": 20,
            "wind_push_probability": 0.0,
        }
    }
    return DroneDeliveryEnv(wind_mode="hidden", config=config, seed=0)


def test_step_reward_and_boundary_penalty():
    env = build_env()
    env.reset(seed=0)
    obs, reward, terminated, truncated, info = env.step(3)
    assert reward < 0
    assert not terminated
    assert not truncated
    assert info["collisions"] >= 1


def test_pickup_reward():
    env = build_env()
    env.reset(seed=0)
    env.position = env.config.pickup_pos
    env.has_package = 0
    env.wind = 0
    obs, reward, terminated, truncated, info = env.step(4)
    assert reward >= 9.0
    assert info["pickup_success"] is True
    assert env.has_package == 1


def test_dropoff_terminal_reward():
    env = build_env()
    env.reset(seed=0)
    env.position = env.config.dropoff_pos
    env.has_package = 1
    env.wind = 0
    obs, reward, terminated, truncated, info = env.step(4)
    assert terminated is True
    assert truncated is False
    assert reward >= 49.0
    assert info["dropoff_success"] is True
