# Hướng dẫn tái lập thí nghiệm

## 1. Cài thư viện

```bash
pip install -r requirements.txt
```

## 2. Chạy train một agent

```bash
python experiments/train.py --algo q_learning --wind-mode observable --seed 0 --config experiments/configs.yaml
```

Các thuật toán hợp lệ:

- `random`
- `heuristic`
- `q_learning`
- `sarsa`
- `double_q_learning`

Hai chế độ state:

- `observable`
- `hidden`

## 3. Chạy evaluate một agent

```bash
python experiments/evaluate.py --algo q_learning --wind-mode observable --seed 0 --config experiments/configs.yaml
```

Evaluation luôn dùng `epsilon = 0`.

## 4. Chạy đủ 10 seed

```bash
python experiments/sweep.py --config experiments/configs.yaml
```

Lệnh này sinh:

- log train trong `results/train/`
- log evaluate trong `results/eval/`
- model trong `results/models/`
- summary từng seed trong `results/summaries/`
- bảng `mean ± std` trong `results/summaries/aggregate_metrics.csv`

## 5. Vẽ biểu đồ

```bash
python visualization/plots.py --results-dir results --output-dir results/figures
```

Biểu đồ đầu ra:

- `learning_curve_observable.png`
- `learning_curve_hidden.png`
- `success_rate_comparison.png`
- `avg_steps_comparison.png`
- `violation_rate_comparison.png`
- `observable_vs_hidden.png`

## 6. Chuẩn bị model cho dashboard (tuỳ chọn)

```bash
python experiments/copy_demo_models.py --results-dir results --seeds 0 1 2
```

## 7. Chạy demo

```bash
streamlit run dashboard/app.py
```

Dashboard có thể tự train trong bộ nhớ nếu chưa có model được pre-train. Kết quả được cache theo `(algo, wind_mode, goal, no_fly, episodes, seed)` — thay đổi bất kỳ tham số nào sẽ trigger train lại.

## 8. Ghi chú về SARSA

SARSA là thuật toán on-policy TD. Khi dùng với dashboard, agent giữ `_pending_action` giữa các bước để đảm bảo cập nhật Q đúng theo hành động thực tế của policy hiện tại (không phải greedy max). Điều này quan trọng để tái lập đúng kết quả khi so sánh với Q-Learning off-policy.
