# Hướng dẫn triển khai chi tiết cho Trần Anh Tuấn

## Vai trò chính

Trần Anh Tuấn phụ trách toàn bộ phần **thực nghiệm, đánh giá, thống kê, biểu đồ và tái lập thí nghiệm**. Đây là phần chứng minh thuật toán hoạt động đúng và kết quả đủ tin cậy để đưa vào báo cáo.

Phần việc này phải trả lời được 5 câu hỏi:

1. Q-Learning có học tốt hơn Random và Heuristic không?
2. Double Q-Learning hoặc SARSA có tốt hơn Q-Learning không?
3. Kết quả có ổn định qua ít nhất 10 seed không?
4. Wind observable có tốt hơn wind hidden không?
5. Thí nghiệm có thể chạy lại được từ đầu không?

---

## 1. Đầu ra bắt buộc

Tuấn cần bàn giao đầy đủ các đầu ra sau:

### 1.1. Mã chạy thí nghiệm

- `experiments/train.py`
- `experiments/evaluate.py`
- `experiments/sweep.py`
- `experiments/configs.yaml`
- module phụ nếu cần như `metrics.py`, `io_utils.py`, `seed_utils.py`

### 1.2. Dữ liệu kết quả

- log train theo episode
- log evaluate theo episode
- file tổng hợp theo từng seed
- file tổng hợp cuối cùng theo từng agent

### 1.3. Bảng và hình cho báo cáo

- bảng `mean ± std`
- learning curve
- success rate chart
- average steps chart
- violation rate chart
- bảng so sánh observable và hidden wind

### 1.4. Tài liệu tái lập

- file hướng dẫn cài môi trường
- file hướng dẫn chạy train
- file hướng dẫn chạy đủ 10 seed
- file hướng dẫn sinh bảng và biểu đồ

---

## 2. Mục tiêu kỹ thuật của phần thực nghiệm

Phần của Tuấn không chỉ là viết script chạy được, mà phải đảm bảo:

- mọi agent được train với cùng budget
- evaluation dùng `epsilon = 0`
- seed được kiểm soát rõ ràng
- metric được định nghĩa nhất quán
- file log đủ chi tiết để truy vết khi số liệu sai
- có thể sinh lại bảng và biểu đồ từ dữ liệu gốc

Nói ngắn gọn, phần này phải đủ chặt để giảng viên nhìn vào thấy nhóm làm RL nghiêm túc chứ không chỉ chạy một lần rồi chụp kết quả đẹp.

---

## 3. Cấu trúc thư mục nên triển khai

```text
drone_delivery/
  experiments/
    train.py
    evaluate.py
    sweep.py
    configs.yaml
    metrics.py
    io_utils.py
    seed_utils.py
  results/
    train/
    eval/
    summaries/
  reports/
    figures/
    reproducibility.md
```

---

## 4. Công việc chi tiết cần làm

## 4.1. Viết `train.py`

### Mục tiêu

Dùng để train **một agent trong một cấu hình cụ thể**.

### Input tối thiểu

- `--algo`: `random`, `heuristic`, `q_learning`, `sarsa`, `double_q_learning`
- `--seed`
- `--config`
- `--wind-mode`: `observable` hoặc `hidden`
- `--output-dir`

### Hyperparameter nên đọc từ config

- `num_episodes`
- `max_steps`
- `alpha`
- `gamma`
- `epsilon_start`
- `epsilon_end`
- `epsilon_decay`
- `eval_interval`
- `moving_average_window`

### Luồng thực thi chuẩn

1. Đọc config.
2. Set global seed.
3. Tạo environment theo `wind-mode`.
4. Tạo agent.
5. Chạy training loop theo số episode.
6. Mỗi episode lưu metric.
7. Lưu model cuối cùng.
8. Lưu file log `.csv` hoặc `.jsonl`.

### Metric phải log theo episode

- `episode`
- `seed`
- `algo`
- `wind_mode`
- `return`
- `steps`
- `success`
- `violations`
- `collisions`
- `pickup_success`
- `dropoff_success`
- `epsilon`

### Những lỗi cần tránh

- train heuristic/random giống RL rồi log sai ý nghĩa
- terminal state vẫn bootstrap Q target
- quên reset seed giữa các lần chạy
- mỗi thuật toán dùng training budget khác nhau

---

## 4.2. Viết `evaluate.py`

### Mục tiêu

Đánh giá agent sau khi train trong chế độ **không khám phá**.

### Yêu cầu cứng

- `epsilon = 0`
- không cập nhật Q-table trong evaluate
- chạy đủ số episode evaluate, ví dụ 100 episode mỗi seed

### Input nên có

- `--algo`
- `--seed`
- `--config`
- `--wind-mode`
- `--model-path`
- `--num-eval-episodes`
- `--output-dir`

### Output nên có

#### File chi tiết theo episode

Ví dụ:

```text
results/eval/q_learning_observable_seed_0.csv
```

#### File tóm tắt cho seed đó

Ví dụ:

```text
results/summaries/q_learning_observable_seed_0_summary.json
```

### Metric cần tính trong evaluate

- `avg_return`
- `std_return`
- `success_rate`
- `avg_steps`
- `std_steps`
- `violation_rate`
- `avg_violations`
- `collision_rate`
- `pickup_rate`
- `dropoff_rate`

### Quy ước khuyến nghị

- `success_rate = số episode thành công / tổng số episode evaluate`
- `violation_rate = số episode có ít nhất 1 vi phạm / tổng số episode`
- `avg_steps = trung bình steps trên toàn bộ episode`

---

## 4.3. Viết `sweep.py`

### Mục tiêu

Tự động chạy toàn bộ thí nghiệm qua 10 seed và gom kết quả.

### Seed bắt buộc

```text
0, 1, 2, 3, 4, 5, 6, 7, 8, 9
```

### Tổ hợp tối thiểu cần chạy

1. Random + Observable
2. Heuristic + Observable
3. Q-Learning + Observable
4. **SARSA + Observable** (thuật toán thứ hai chính)
5. Q-Learning + Hidden
6. SARSA + Hidden

Nếu nhóm muốn mạnh hơn, có thể thêm:

- Double Q-Learning + Observable / Hidden
- Heuristic + Hidden
- Random + Hidden

### Luồng chạy nên là

Với mỗi tổ hợp `(algo, wind_mode, seed)`:

1. train
2. evaluate
3. lưu log train
4. lưu log evaluate
5. lưu summary seed-level

Sau khi xong toàn bộ:

6. gom các summary
7. tính `mean ± std`
8. ghi bảng tổng hợp cuối

---

## 5. Định nghĩa chỉ số và cách tính

## 5.1. Reward / Return

- `episode_return`: tổng reward nhận được trong một episode
- `avg_return`: trung bình của `episode_return` qua các episode evaluate

## 5.2. Success rate

Một episode được tính là thành công nếu agent giao hàng xong đúng luật trước khi bị truncated.

\[
\text{success rate} = \frac{\text{số episode thành công}}{\text{tổng số episode evaluate}}
\]

## 5.3. Average steps

\[
\text{avg steps} = \frac{\sum \text{steps per episode}}{N}
\]

## 5.4. Violation rate

Nếu một episode có ít nhất một lần vào no-fly zone thì có thể đánh dấu là một episode vi phạm.

\[
\text{violation rate} = \frac{\text{số episode có vi phạm}}{N}
\]

Ngoài ra nên lưu thêm:

- `avg_violations_per_episode`

## 5.5. Collision count

Nếu drone đâm biên hoặc obstacle thì tăng collision count. Nên lưu theo episode và tính trung bình.

---

## 6. Công thức `mean ± std`

Sau khi đã có 10 giá trị seed-level cho một metric, ví dụ success rate:

\[
\mu = \frac{1}{10}\sum_{i=1}^{10} x_i
\]

\[
\sigma = \sqrt{\frac{1}{10}\sum_{i=1}^{10}(x_i - \mu)^2}
\]

### Quy tắc trình bày

- phần trăm: `84.2 ± 5.1 %`
- số bước: `23.8 ± 2.7`
- return: `31.4 ± 6.2`

### Điều quan trọng

Phải dùng **cùng một cách tính std** ở toàn bộ bảng và biểu đồ. Không được chỗ này dùng population std, chỗ khác dùng sample std mà không nói rõ.

---

## 7. Cấu trúc file kết quả khuyến nghị

```text
results/
  train/
    q_learning_observable_seed_0.csv
    q_learning_observable_seed_1.csv
  eval/
    q_learning_observable_seed_0.csv
    q_learning_observable_seed_1.csv
  summaries/
    q_learning_observable_seed_0.json
    q_learning_observable_seed_1.json
    aggregate_metrics.csv
```

### Mẫu cột file train log

```text
episode,seed,algo,wind_mode,return,steps,success,violations,collisions,epsilon
```

### Mẫu cột file eval log

```text
episode,seed,algo,wind_mode,return,steps,success,violations,collisions,pickup_success,dropoff_success
```

### Mẫu key của file summary JSON

```json
{
  "algo": "q_learning",
  "wind_mode": "observable",
  "seed": 0,
  "num_eval_episodes": 100,
  "avg_return": 31.2,
  "std_return": 5.8,
  "success_rate": 0.84,
  "avg_steps": 24.1,
  "std_steps": 3.2,
  "violation_rate": 0.09,
  "avg_violations": 0.12,
  "collision_rate": 0.05
}
```

---

## 8. Bảng kết quả đánh giá cần làm

## 8.1. Bảng chính cho báo cáo

| Agent | Wind mode | Success rate | Avg return | Avg steps | Violation rate |
|------|------|------:|------:|------:|------:|
| Random | Observable | mean ± std | mean ± std | mean ± std | mean ± std |
| Heuristic | Observable | mean ± std | mean ± std | mean ± std | mean ± std |
| Q-Learning | Observable | mean ± std | mean ± std | mean ± std | mean ± std |
| SARSA | Observable | mean ± std | mean ± std | mean ± std | mean ± std |
| Q-Learning | Hidden | mean ± std | mean ± std | mean ± std | mean ± std |
| SARSA | Hidden | mean ± std | mean ± std | mean ± std | mean ± std |

Nếu có thêm Double Q-Learning, bổ sung thêm 2 dòng tương tự.

## 8.2. Bảng phụ nên có

### Bảng so sánh từng seed

| Seed | Agent | Wind mode | Success rate | Avg return | Avg steps |
|------:|------|------|------:|------:|------:|
| 0 | Q-Learning | Observable | ... | ... | ... |
| 1 | Q-Learning | Observable | ... | ... | ... |

Bảng này giúp kiểm tra độ ổn định và giải thích nếu có seed bất thường.

---

## 9. Biểu đồ cần vẽ

## 9.1. Learning curve

### Nội dung

- trục X: episode
- trục Y: average return hoặc moving average return
- mỗi agent một đường riêng

### Nên có 2 biểu đồ

- observable setting
- hidden setting

### Lưu ý

- nếu nhiễu quá mạnh, dùng moving average window 50 hoặc 100 episode
- phải ghi rõ smoothing window trong caption

## 9.2. Biểu đồ success rate

Dùng bar chart để so sánh:

- Random
- Heuristic
- Q-Learning
- Double Q

Có thể thêm error bar = std.

## 9.3. Biểu đồ average steps

Dùng bar chart, càng thấp càng tốt nếu success vẫn cao.

## 9.4. Biểu đồ violation rate

Dùng bar chart để cho thấy agent nào an toàn hơn.

## 9.5. Biểu đồ observable vs hidden

Dùng grouped bar chart cho 2 biến thể state với cùng thuật toán để cho thấy ảnh hưởng của thiếu thông tin về gió.

### Tên file nên sinh

```text
reports/figures/
  learning_curve_observable.png
  learning_curve_hidden.png
  success_rate_comparison.png
  avg_steps_comparison.png
  violation_rate_comparison.png
  observable_vs_hidden_q_learning.png
  observable_vs_hidden_double_q.png
```

---

## 10. Nội dung bắt buộc trong `configs.yaml`

Nên có các nhóm cấu hình sau:

### Environment

- `grid_rows: 7`
- `grid_cols: 7`
- `max_steps`
- `pickup_position`
- `dropoff_position`
- `no_fly_zones`
- `wind_transition_matrix`
- `wind_push_probability`

### Training

- `num_episodes`
- `alpha`
- `gamma`
- `epsilon_start`
- `epsilon_end`
- `epsilon_decay`

### Evaluation

- `num_eval_episodes`
- `eval_epsilon: 0.0`

### Logging

- `save_train_logs: true`
- `save_eval_logs: true`
- `save_plots: true`

---

## 11. Hướng dẫn tái lập thí nghiệm phải viết

Tuấn cần tạo một file như:

```text
reports/reproducibility.md
```

Nội dung nên có 6 phần.

## 11.1. Yêu cầu môi trường

- Python version
- thư viện cần cài
- cách tạo virtual env

Ví dụ:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## 11.2. Cấu hình mặc định

Ghi rõ file nào chứa hyperparameter chính.

Ví dụ:

- `experiments/configs.yaml`

## 11.3. Chạy train một model

Ví dụ:

```bash
python experiments/train.py --algo q_learning --wind-mode observable --seed 0 --config experiments/configs.yaml
```

## 11.4. Chạy evaluate một model

Ví dụ:

```bash
python experiments/evaluate.py --algo q_learning --wind-mode observable --seed 0 --config experiments/configs.yaml
```

## 11.5. Chạy đủ 10 seed

Ví dụ:

```bash
python experiments/sweep.py --config experiments/configs.yaml
```

## 11.6. Sinh bảng và biểu đồ

Ví dụ:

```bash
python visualization/plots.py
```

---

## 12. Phân chia công việc cụ thể theo ngày

## Ngày 1

- chốt format log
- chốt metric
- viết `train.py`
- test train với 1 seed, 20 episode nhỏ

## Ngày 2

- viết `evaluate.py`
- kiểm tra `epsilon = 0`
- xuất file summary cho 1 seed

## Ngày 3

- viết `sweep.py`
- chạy Q-Learning observable đủ 10 seed
- kiểm tra thư mục kết quả

## Ngày 4

- chạy Double Q hoặc SARSA
- chạy hidden wind
- gom bảng kết quả sơ bộ

## Ngày 5

- vẽ biểu đồ
- rà lại mean ± std
- viết `reproducibility.md`
- đối chiếu số liệu với nhóm viết báo cáo

---

## 13. Checklist nghiệm thu nội bộ cho phần Tuấn

- [ ] `train.py` chạy được với mọi agent cần thiết
- [ ] `evaluate.py` chạy đúng với `epsilon = 0`
- [ ] `sweep.py` chạy đủ 10 seed
- [ ] log được lưu riêng theo từng seed
- [ ] summary được lưu riêng theo từng seed
- [ ] có file aggregate cuối cùng
- [ ] bảng báo cáo dùng `mean ± std`
- [ ] có learning curve
- [ ] có success rate chart
- [ ] có avg steps chart
- [ ] có violation rate chart
- [ ] có so sánh observable và hidden
- [ ] có tài liệu tái lập thí nghiệm
- [ ] người khác chạy theo hướng dẫn có thể ra lại kết quả cùng xu hướng

---

## 14. Tiêu chí hoàn thành cuối cùng

Phần của Trần Anh Tuấn được xem là hoàn thành khi:

- toàn bộ pipeline train → evaluate → sweep → aggregate → plot chạy thông suốt
- kết quả của tất cả agent được báo cáo trên ít nhất 10 seed
- bảng kết quả có `mean ± std`
- biểu đồ đủ dùng cho báo cáo và demo
- có tài liệu tái lập thí nghiệm rõ ràng
- số liệu có thể truy ngược về log gốc mà không mâu thuẫn
