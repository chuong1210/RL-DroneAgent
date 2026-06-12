# HƯỚNG DẪN CHẠY DỰ ÁN DRONE GIAO HÀNG TRONG GIÓ

## 1. Mục tiêu
Dự án này mô phỏng bài toán **drone giao hàng trong môi trường có gió** và so sánh các thuật toán:
- Random Agent
- Heuristic Agent
- Q-Learning
- SARSA (on-policy TD)
- Double Q-Learning

Hệ thống gồm 2 phần chính:
- **Dashboard Streamlit** — demo trực quan, train inline, so sánh thuật toán
- **Experiments pipeline** — train/evaluate theo seed để lấy số liệu báo cáo

---

## 2. Chuẩn bị môi trường
Yêu cầu:
- Python 3.10+
- pip đã cài sẵn

Cài thư viện:

```bash
pip install -r requirements.txt
```

---

## 3. Cấu trúc quan trọng
- `envs/` : môi trường drone
- `agents/` : random, heuristic, q_learning, sarsa, double_q_learning, factory
- `experiments/train.py` : train 1 mô hình và lưu log/model
- `experiments/evaluate.py` : đánh giá 1 mô hình (epsilon = 0)
- `experiments/sweep.py` : chạy toàn bộ thí nghiệm nhiều seed
- `dashboard/app.py` : giao diện demo Streamlit 5 tab
- `results/` : nơi lưu log, model, metrics, figures

---

## 4. Mở dashboard để demo (cách nhanh nhất)

Chỉ cần một lệnh:

```bash
streamlit run dashboard/app.py
```

Mở trình duyệt tại:

```text
http://localhost:8501
```

**Dashboard tự train agent trong bộ nhớ** khi cần — không cần chạy `train.py` trước. Lần đầu mở sẽ có spinner "Đang train..." mất vài giây, sau đó kết quả được cache.

---

## 5. Các tab trong dashboard

### Tab Mô phỏng
- Chọn thuật toán: SARSA, Q-Learning, Double Q-Learning, Heuristic, Random.
- Chọn Goal: G0 (0,6) · G1 (3,6) · G2 (6,0).
- Chọn Bản đồ: Cố định hoặc Medium (no-fly ngẫu nhiên).
- Điều khiển: Chạy thuật toán (auto step) · Bước tiếp · Dừng · Episode mới.
- Tốc độ auto: thanh trượt 50–1000ms/bước.
- Bảng THÔNG TIN bên phải: vị trí, hướng, khoảng cách, reward, trạng thái gói hàng.
- Thống kê nhanh: Episode / Thành công / Tỷ lệ %.
- Drone hiển thị bay lơ lửng phía trên lưới với bóng đổ và hiệu ứng rotor glow.

### Tab Learning Curves
- Đường cong reward (moving average) và success rate (%) theo episode.
- So sánh 4 thuật toán: Random, Heuristic, Q-Learning, SARSA.
- Đường Target 85% trên biểu đồ success rate.

### Tab So sánh
- 3 bar chart: Success Rate (%) · Avg Steps (±std) · Collision Rate (%).
- Đánh giá greedy (ε=0) tự động cho 4 thuật toán.

### Tab Replay
- Phát lại một episode hoàn chỉnh với seed tùy chọn.
- Điều chỉnh delay mỗi bước.

### Tab Cài đặt
- Số episode huấn luyện (500–5000).
- Chế độ gió: observable / hidden.
- Cửa sổ trung bình trượt, target success rate.
- Xóa cache và train lại toàn bộ.

---

## 6. Chạy train một mô hình (cho số liệu báo cáo)

Ví dụ train Q-Learning với wind observable, seed 0:

```bash
python experiments/train.py --algo q_learning --wind-mode observable --seed 0
```

Ví dụ train SARSA:

```bash
python experiments/train.py --algo sarsa --wind-mode observable --seed 0
```

Ví dụ train Double Q-Learning:

```bash
python experiments/train.py --algo double_q_learning --wind-mode observable --seed 0
```

Các thuật toán hợp lệ: `random`, `heuristic`, `q_learning`, `sarsa`, `double_q_learning`

Sau khi train xong sẽ sinh ra:
- file log trong `results/train/`
- file model trong `results/models/`

---

## 7. Đánh giá một mô hình

```bash
python experiments/evaluate.py --algo q_learning --wind-mode observable --seed 0
```

Evaluation luôn dùng `epsilon = 0`. Kết quả lưu trong `results/eval/` và `results/summaries/`.

---

## 8. Chạy toàn bộ thí nghiệm nhiều seed

```bash
python experiments/sweep.py --config experiments/configs.yaml
```

Lệnh này sẽ:
- train tất cả agent (kể cả SARSA)
- evaluate tất cả agent
- tổng hợp mean ± std
- tạo bảng so sánh kết quả

Kết quả quan trọng nằm ở:
- `results/summaries/aggregate_metrics.csv`
- `results/summaries/seed_level_metrics.csv`

---

## 9. Quy trình demo nhanh trên lớp

### Bước 1: Cài thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Mở dashboard
```bash
streamlit run dashboard/app.py
```

### Bước 3: Trong dashboard

**Mô phỏng tốt nhất:**
- Tab Mô phỏng → chọn **SARSA** hoặc **Q-Learning** → Goal **G0** → Bản đồ Cố định → **Chạy thuật toán**

**So sánh algorithms:**
- Tab Learning Curves — thấy đường cong SARSA/Q-Learning hội tụ nhanh hơn Random/Heuristic

**Bar chart kết quả:**
- Tab So sánh — 3 biểu đồ success rate, avg steps, collision rate

**Replay nhiều seed:**
- Tab Replay → chọn seed 0, 1, 2 → Phát replay

---

## 10. Giải thích nhanh các tham số quan trọng

Trong `experiments/configs.yaml`:
- `num_episodes`: số episode train
- `alpha`: learning rate
- `gamma`: discount factor
- `epsilon_start`: xác suất khám phá ban đầu
- `epsilon_end`: xác suất khám phá nhỏ nhất
- `epsilon_decay`: tốc độ giảm epsilon

Lưu ý:
- observable thường học tốt hơn hidden vì agent nhìn thấy trạng thái gió
- SARSA là on-policy (dùng action thực tế của agent), Q-Learning là off-policy (dùng max Q)

---

## 11. Trường hợp train ra kết quả xấu

### Chưa đủ số episode
```bash
python experiments/train.py --algo q_learning --wind-mode observable --seed 0 --episodes 3000
```

### Chọn hidden mode
`hidden` khó hơn `observable`. Khi demo nên ưu tiên `observable`.

### Agent yếu cho demo
- `random` chỉ để làm baseline
- `heuristic` tốt hơn random nhưng không học được
- `sarsa` và `q_learning` nên dùng để trình bày kết quả chính

---

## 12. Kết quả nên nhấn mạnh khi thuyết trình

- RL (SARSA, Q-Learning) tốt hơn Random và Heuristic
- Observable tốt hơn Hidden — vì state có thêm biến gió
- SARSA là thuật toán on-policy, Q-Learning là off-policy — cả hai đều hội tụ
- Dashboard cho thấy trực quan drone bay, learning curve và so sánh thuật toán

---

## 13. Lệnh ngắn gọn cần nhớ

Mở dashboard:
```bash
streamlit run dashboard/app.py
```

Train đầy đủ 10 seed:
```bash
python experiments/sweep.py --config experiments/configs.yaml
```

Train nhanh 1 model:
```bash
python experiments/train.py --algo sarsa --wind-mode observable --seed 0
```
