from experiments.evaluate import evaluate_agent
from experiments.io_utils import load_config
from experiments.train import train_agent


def test_train_and_evaluate_mini_pipeline(tmp_path):
    config = load_config("experiments/configs.yaml")
    config["training"]["num_episodes"] = 20
    config["evaluation"]["num_eval_episodes"] = 5
    result = train_agent("q_learning", "hidden", 0, config, output_dir=tmp_path, episodes=20)
    assert result["model_path"] is not None
    eval_result = evaluate_agent("q_learning", "hidden", 0, config, output_dir=tmp_path, model=result["model_path"], episodes=5)
    assert eval_result["summary"]["num_episodes"] == 5
    assert "success_rate" in eval_result["summary"]
