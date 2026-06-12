from envs import DroneDeliveryEnv


def test_observable_encoder_decoder_roundtrip():
    env = DroneDeliveryEnv(wind_mode="observable", seed=0)
    for r in range(env.config.rows):
        for c in range(env.config.cols):
            for wind in range(env.num_winds):
                for has_package in [0, 1]:
                    state = (r, c, wind, has_package)
                    encoded = env.state_encoder(state)
                    decoded = env.state_decoder(encoded)
                    assert decoded == state


def test_hidden_encoder_decoder_roundtrip():
    env = DroneDeliveryEnv(wind_mode="hidden", seed=0)
    for r in range(env.config.rows):
        for c in range(env.config.cols):
            for has_package in [0, 1]:
                state = (r, c, has_package)
                encoded = env.state_encoder(state)
                decoded = env.state_decoder(encoded)
                assert decoded == state
