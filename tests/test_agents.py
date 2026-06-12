from agents.double_q_learning import DoubleQLearningAgent
from agents.heuristic_agent import HeuristicAgent
from agents.q_learning import QLearningAgent
from agents.random_agent import RandomAgent
from envs import DroneDeliveryEnv


def test_random_action_range():
    env = DroneDeliveryEnv(wind_mode="hidden", seed=0)
    agent = RandomAgent(num_actions=env.num_actions, seed=0)
    for _ in range(20):
        action = agent.select_action(None)
        assert 0 <= action < env.num_actions


def test_heuristic_prefers_goal_direction():
    env = DroneDeliveryEnv(wind_mode="hidden", seed=0)
    agent = HeuristicAgent(env, seed=0)
    state = (6, 0, 0)
    action = agent.select_action(state)
    assert action in range(env.num_actions)


def test_q_learning_update_changes_value():
    agent = QLearningAgent(num_states=10, num_actions=5, alpha=0.5, gamma=0.9, seed=0)
    agent.update(0, 1, 1.0, 2, terminated=False)
    assert agent.q_table[0, 1] > 0


def test_double_q_learning_update_changes_value():
    agent = DoubleQLearningAgent(num_states=10, num_actions=5, alpha=0.5, gamma=0.9, seed=0)
    agent.update(0, 1, 1.0, 2, terminated=False)
    assert (agent.q1[0, 1] > 0) or (agent.q2[0, 1] > 0)
