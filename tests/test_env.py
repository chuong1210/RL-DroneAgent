from envs import DroneDeliveryEnv


def test_reset_and_step_shapes():
    env = DroneDeliveryEnv(wind_mode="observable", seed=1)
    obs, info = env.reset(seed=1)
    assert len(obs) == 4
    next_obs, reward, terminated, truncated, info = env.step(4)
    assert len(next_obs) == 4
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)


def test_invalid_action_raises():
    env = DroneDeliveryEnv(wind_mode="hidden", seed=1)
    env.reset(seed=1)
    try:
        env.step(99)
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_max_steps_truncates():
    config = {"environment": {"max_steps": 2, "wind_push_probability": 0.0}}
    env = DroneDeliveryEnv(wind_mode="hidden", config=config, seed=1)
    env.reset(seed=1)
    env.step(4)
    obs, reward, terminated, truncated, info = env.step(4)
    assert truncated is True
    assert terminated is False
