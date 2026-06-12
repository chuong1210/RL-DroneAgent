from agents.q_learning import QLearningAgent
from envs import DroneDeliveryEnv


def test_q_learning_terminal_no_bootstrap():
    env = DroneDeliveryEnv(wind_mode="hidden", seed=0)
    agent = QLearningAgent(env.num_states, env.num_actions, alpha=1.0, gamma=0.99, seed=0)
    state = 0
    next_state = 1
    agent.q_table[next_state, :] = 5.0
    agent.update(state, 2, 3.0, next_state, terminated=True)
    assert agent.q_table[state, 2] == 3.0
