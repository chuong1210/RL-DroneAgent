# Drone Delivery in Wind

Dự án RL tự cài cho đề tài Drone giao hàng trong gió.

## Thành phần chính

- Môi trường grid 7x7 tự viết với gió Markov stochastic.
- Wind observable và wind hidden.
- Random Agent.
- Heuristic Agent.
- Q-Learning.
- SARSA (on-policy TD).
- Double Q-Learning.
- Train/evaluate/sweep 10 seed.
- Bảng `mean ± std`.
- Biểu đồ learning curve, success rate, average steps, violation rate.
- Dashboard Streamlit 5 tab: Mô phỏng · Learning Curves · So sánh · Replay · Cài đặt.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Smoke test nhanh

```bash
python experiments/train.py --algo q_learning --wind-mode hidden --seed 0 --episodes 30
python experiments/evaluate.py --algo q_learning --wind-mode hidden --seed 0 --episodes 5
```

## Chạy đầy đủ 10 seed

```bash
python experiments/sweep.py --config experiments/configs.yaml
python visualization/plots.py --results-dir results --output-dir results/figures
```

## Chạy dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard tự train các agent trong bộ nhớ khi mở lần đầu — không cần chạy `train.py` trước.

## Cấu trúc

```text
drone_delivery/
  envs/               # môi trường DroneDeliveryEnv
  agents/             # random, heuristic, q_learning, sarsa, double_q_learning, factory
  experiments/        # train.py, evaluate.py, sweep.py, configs.yaml
  visualization/      # plots.py, policy_visualizer.py
  dashboard/
    app.py            # Streamlit 5-tab dashboard
    components/       # grid_display, info_panel, learning_curve, comparison_charts
  tests/
  reports/
```
"# RL-DroneAgent" 
