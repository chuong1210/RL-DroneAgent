# Hướng dẫn chi tiết chuẩn chung và báo cáo cho đề tài Drone giao hàng trong gió

## 1. Mục đích tài liệu

Tài liệu này tổng hợp:

- Chuẩn chung bắt buộc của môn cho mọi đề tài RL.
- Cách áp dụng các chuẩn đó vào **Đề tài 6: Drone giao hàng trong gió**.
- Khung báo cáo chi tiết để nhóm có thể dùng trực tiếp khi viết báo cáo cuối kỳ.
- Checklist nghiệm thu nhanh để tự rà soát trước khi nộp.

---

## 2. Chuẩn chung bắt buộc cho mọi đề tài

### 2.1. Phạm vi bắt buộc

Nhóm phải **tự phát triển từ đầu** các thành phần sau.

#### 2.1.1. Môi trường RL tự viết

Môi trường phải có đầy đủ:

- `reset(seed)`
- `step(action)`
- `render()`
- `state_encoder()`
- `state_decoder()`

Ngoài ra phải có:

- kiểm thử transition
- kiểm thử reward
- kiểm thử terminal state
- seed để tái lập thực nghiệm

Lưu ý quan trọng:

- Có thể tham khảo cách tổ chức API của Gymnasium.
- Không được dùng môi trường Gymnasium có sẵn làm môi trường chính của bài.

#### 2.1.2. Thuật toán tự cài

Nhóm phải tự cài ít nhất các agent sau:

- Random Agent
- Heuristic Agent
- Q-Learning
- **SARSA** (on-policy TD — đã cài, dùng làm biến thể thứ hai chính)
- Double Q-Learning (đã cài, có sẵn trong dashboard và sweep)
- Epsilon-greedy exploration
- Evaluation mode với `epsilon = 0`

Không được dùng:

- Stable-Baselines
- RLlib
- CleanRL
- thư viện agent RL có sẵn

#### 2.1.3. Đánh giá bắt buộc

Thực nghiệm phải có:

- ít nhất **10 seed**
- báo cáo **mean ± std**
- learning curve
- success rate hoặc task completion rate
- số bước trung bình
- số lỗi hoặc số lần vi phạm ràng buộc
- so sánh giữa Random, Heuristic, Q-Learning và biến thể thứ hai

Không được đánh giá bằng một lần chạy duy nhất.

#### 2.1.4. Demo bắt buộc

Demo phải:

- chạy được agent sau khi học
- hiển thị trạng thái hiện tại
- hiển thị hành động được chọn
- hiển thị reward tức thời
- hiển thị policy bằng mũi tên, bảng hoặc heatmap
- hiển thị đường học
- có tùy chọn chuyển giữa Random, Heuristic và RL Agent

---

## 3. Những điểm phải chốt trước khi cài môi trường

Khi tự thiết kế môi trường RL, nhóm phải trả lời rõ các câu hỏi sau:

1. **Agent học kỹ năng gì?**  
   Ví dụ: đi đến đích nhanh, tránh vùng cấm, thích nghi với gió ngẫu nhiên.

2. **Agent quan sát được gì?**  
   Quan sát có đủ thông tin để ra quyết định không.

3. **Action space là gì?**  
   Có action nào invalid không, nếu có thì xử lý ra sao.

4. **Đo thành công như thế nào?**  
   Ví dụ: giao hàng thành công, tỷ lệ vi phạm thấp, đường đi ngắn.

5. **Episode kết thúc khi nào?**  
   Khi giao hàng thành công, hết số bước tối đa, hoặc vi phạm điều kiện dừng nào đó.

---

## 4. Công thức lõi bắt buộc phải giải thích trong báo cáo

### 4.1. Công thức cập nhật Q-Learning

\[
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[r_{t+1} + \gamma \max_a Q(s_{t+1}, a) - Q(s_t, a_t)\right]
\]

### 4.2. Những thành phần phải giải thích

Trong báo cáo, nhóm phải giải thích được:

- **\(\alpha\)**: tốc độ học, quyết định mức độ cập nhật giá trị cũ theo thông tin mới.
- **\(\gamma\)**: hệ số chiết khấu, đo mức độ coi trọng phần thưởng tương lai.
- **TD target**:  
  \[
  r_{t+1} + \gamma \max_a Q(s_{t+1}, a)
  \]
- **TD error**: phần chênh lệch giữa target và giá trị hiện tại.
- Nếu **\(s_{t+1}\)** là terminal thì target chỉ còn **\(r_{t+1}\)**.

### 4.3. Điều phải làm đúng khi cài đặt

- Nếu trạng thái tiếp theo là terminal thì **không bootstrap** từ `max Q(s_{t+1}, a)`.
- Evaluation phải dùng `epsilon = 0`.
- Training và evaluation phải tách riêng.

---

## 5. Cấu trúc mã nguồn tối thiểu khuyến nghị

```text
project_name/
  envs/
    base_env.py
    custom_env.py
  agents/
    random_agent.py
    heuristic_agent.py
    q_learning.py
    sarsa.py
    double_q_learning.py
  experiments/
    train.py
    evaluate.py
    sweep.py
    configs.yaml
  visualization/
    render.py
    plots.py
  dashboard/
    app.py
  tests/
    test_env.py
    test_encoder.py
    test_rewards.py
  reports/
    figures/
    final_report.pdf
```

### 5.1. Ánh xạ thực tế trong dự án

- `envs/drone_delivery_env.py`: môi trường drone bay trong grid 7×7 có gió Markov
- `agents/random_agent.py`: agent hành động ngẫu nhiên
- `agents/heuristic_agent.py`: agent đi gần đích và tránh vùng cấm theo luật tay
- `agents/q_learning.py`: Q-Learning (off-policy)
- `agents/sarsa.py`: SARSA (on-policy TD, dùng `_pending_action` state machine)
- `agents/double_q_learning.py`: Double Q-Learning
- `agents/factory.py`: `create_agent(algo, env, config, seed)` — factory chung cho mọi agent
- `experiments/train.py`: train từng agent, lưu log/model
- `experiments/evaluate.py`: chạy evaluation với `epsilon = 0`
- `experiments/sweep.py`: chạy 10 seed và gom kết quả
- `visualization/render.py`: render map, drone, gió, vùng cấm, đường bay
- `visualization/plots.py`: vẽ learning curve, bar chart, violation rate
- `dashboard/app.py`: Streamlit 5 tab — Mô phỏng · Learning Curves · So sánh · Replay · Cài đặt
- `dashboard/components/grid_display.py`: render lưới + drone hover effect (shadow, glow, sinusoidal bob)
- `dashboard/components/info_panel.py`: bảng THÔNG TIN bên phải
- `dashboard/components/learning_curve.py`: biểu đồ reward và success rate MA
- `dashboard/components/comparison_charts.py`: 3 bar chart so sánh thuật toán
- `tests/`: kiểm thử transition, reward, terminal, encoder/decoder, seed

---

## 6. Kế hoạch phát triển tối thiểu theo tiến độ môn

### Giai đoạn 1

- Chốt MDP
- Viết môi trường
- Viết encoder/decoder
- Viết Random Agent
- Kiểm thử transition

### Giai đoạn 2

- Cài Q-Learning
- Cài epsilon schedule
- Cài logging
- Chạy bản nhỏ để kiểm tra pipeline

### Giai đoạn 3

- Cài Double Q-Learning hoặc SARSA
- Chạy 10 seed
- Chỉnh reward nếu cần
- So sánh với baseline

### Giai đoạn 4

- Hoàn thiện demo
- Vẽ policy
- Viết báo cáo
- Quay video demo

---

## 7. Đặc tả chi tiết cho đề tài 6: Drone giao hàng trong gió

## 7.1. Mục tiêu bài toán

Drone di chuyển trong một lưới 7x7 để:

- đi đến điểm pickup
- lấy hàng
- đi đến điểm dropoff
- thả hàng thành công

Khó khăn chính là **gió ngẫu nhiên** làm drone bị lệch hướng, khiến transition có tính stochastic. Agent cần học được policy ổn định dưới nhiễu này.

---

## 7.2. MDP của đề tài

### 7.2.1. State

Đề bài gốc đề xuất:

\[
s = (r, c, wind, has\_package)
\]

Trong đó:

- `r`: hàng hiện tại của drone
- `c`: cột hiện tại của drone
- `wind ∈ {calm, north, east, west}`
- `has_package ∈ {0,1}`

Số lượng state nếu pickup và dropoff cố định:

\[
49 \times 4 \times 2 = 392
\]

### 7.2.2. Hai biến thể quan sát

Nhóm nên làm đúng theo yêu cầu đề tài:

#### Biến thể A: Wind observable

State đầy đủ:

\[
(r, c, wind, has\_package)
\]

Ý nghĩa:

- Agent biết trạng thái gió hiện tại.
- Bài toán gần với MDP đầy đủ hơn.
- Kỳ vọng học tốt hơn.

#### Biến thể B: Wind hidden

State rút gọn:

\[
(r, c, has\_package)
\]

Ý nghĩa:

- Agent không quan sát được gió.
- Khi đó thông tin bị thiếu, giả định Markov yếu hơn.
- Kết quả kỳ vọng thấp hơn hoặc đường đi dài hơn.

### 7.2.3. Action

Action space đề xuất:

- `up`
- `right`
- `down`
- `left`
- `wait`

Nhóm nên mã hóa action dạng số nguyên, ví dụ:

- `0 = up`
- `1 = right`
- `2 = down`
- `3 = left`
- `4 = wait`

### 7.2.4. Transition

Quy trình transition nên được định nghĩa rõ ràng và nhất quán.

Một quy trình hợp lý:

1. Agent chọn action.
2. Drone thực hiện dịch chuyển theo action.
3. Gió hiện tại có thể đẩy drone thêm một ô theo hướng gió với xác suất nhất định.
4. Nếu vị trí sau action hoặc sau gió đi ra ngoài map hay vào obstacle thì drone đứng yên hoặc bị chặn theo luật đã định.
5. Tính reward từ trạng thái kết quả cuối cùng.
6. Cập nhật gió tiếp theo theo ma trận chuyển `P(w_{t+1} | w_t)`.

### 7.2.5. Wind transition

Nhóm nên cài ma trận chuyển gió Markov như đề bài gợi ý:

- Giữ nguyên gió hiện tại: `0.7`
- Chuyển sang mỗi trạng thái gió khác: `0.1`

Ví dụ nếu `wind = north` thì:

- `P(north | north) = 0.7`
- `P(calm | north) = 0.1`
- `P(east | north) = 0.1`
- `P(west | north) = 0.1`

Điểm cần nêu rõ trong báo cáo:

- Gió hiện tại ảnh hưởng thế nào đến vị trí drone.
- Gió được cập nhật ở thời điểm nào trong `step()`.
- Reward được tính trước hay sau khi hoàn tất transition vật lý.

### 7.2.6. Reward

Reward đề xuất từ đề bài:

- Mỗi bước: `-1`
- Vào no-fly zone: `-20`
- Pickup đúng: `+10`
- Dropoff đúng: `+50`, terminal
- `wait`: `-0.5`
- Drop/pick sai: `-5`

### 7.2.7. Terminal và truncated

Nên định nghĩa rõ:

#### Terminal

Episode kết thúc thực sự khi:

- drone đã pickup đúng
- drone đến đúng điểm dropoff
- thực hiện dropoff đúng
- giao hàng thành công

#### Truncated

Episode bị cắt khi:

- vượt quá số bước tối đa, ví dụ `max_steps = 100` hoặc `150`

Cần phân biệt rõ trong code và báo cáo:

- `terminated = True`: hoàn thành mục tiêu
- `truncated = True`: dừng kỹ thuật do hết budget bước

---

## 8. Các quyết định thiết kế nên chốt rõ trong báo cáo

## 8.1. Pickup và dropoff có cần action riêng hay không

Có hai cách hợp lý:

### Cách 1: Tự động pickup/dropoff theo vị trí

- Nếu drone đứng đúng ô pickup và chưa có hàng thì tự động pickup.
- Nếu drone đứng đúng ô dropoff và đang có hàng thì tự động dropoff.

Ưu điểm:

- State-action space đơn giản.
- Dễ học hơn.

Nhược điểm:

- Không thể dùng reward `drop/pick sai: -5` đúng nghĩa vì không có action pick/drop riêng.

### Cách 2: Có thêm action `pick` và `drop`

- Khi ở đúng ô pickup mới pick thành công.
- Khi ở đúng ô dropoff và đang có hàng mới drop thành công.

Ưu điểm:

- Khớp logic đề bài hơn.
- Dùng được reward sai thao tác.

Nhược điểm:

- Action space lớn hơn.
- Học khó hơn.

**Khuyến nghị thực tế:** Nếu nhóm muốn bám sát reward đề bài thì nên thêm action `pick` và `drop`. Nếu nhóm muốn giữ đúng action set đề bài đã nêu, cần ghi rõ rằng pickup/dropoff là tự động khi vào đúng ô.

## 8.2. Invalid action xử lý thế nào

Ví dụ invalid:

- đi ra ngoài map
- đi vào obstacle
- hành động pick khi không ở ô pickup
- hành động drop khi không ở ô dropoff hoặc chưa có hàng

Cần chốt một trong hai hướng:

- **Phạt và giữ nguyên vị trí**
- **Action mask**

Vì checklist môn có nhắc trực tiếp, báo cáo cần nói rõ nhóm dùng cách nào.

## 8.3. Reward cho wait

Đề bài cảnh báo lỗi phổ biến: `wait` quá lợi khiến agent đứng yên.

Do đó cần:

- giữ `wait` ít hấp dẫn hơn tiến tới mục tiêu
- kiểm tra sau training xem agent có bị loop đứng yên không
- báo cáo tỷ lệ dùng `wait` hoặc trực quan policy để chứng minh không bị exploit reward

---

## 9. Yêu cầu kết quả riêng cho đề tài drone

Nhóm cần đạt hoặc giải thích được các kết quả sau:

### 9.1. Với wind observable

- Success rate kỳ vọng **≥ 80%**
- Policy ổn định hơn
- Đường đi hợp lý hơn

### 9.2. Với wind hidden

- Kết quả phải thấp hơn hoặc số bước dài hơn
- Nhóm phải giải thích rằng state thiếu biến `wind` nên thông tin không đầy đủ
- Đây là điểm quan trọng để phân tích tính Markov

### 9.3. Chỉ số bắt buộc nên báo cáo thêm

Ngoài success rate và reward, nên có:

- collision rate hoặc số lần va chạm biên/obstacle
- no-fly violation rate
- số bước trung bình mỗi episode
- pickup success rate
- dropoff success rate
- average return

---

## 10. Demo bắt buộc cho đề tài drone

Dashboard Streamlit 5 tab (`dashboard/app.py`) đã đáp ứng đầy đủ các yêu cầu demo.

### 10.1. Hiển thị môi trường ✅

Tab **Mô phỏng** — cột giữa:
- grid 7×7
- drone hiển thị bay lơ lửng với bóng đổ và vòng sáng rotor (hover effect)
- P = pickup (màu vàng), G = dropoff (màu xanh), ✕ = no-fly (màu đỏ)
- đường bay đã đi (trajectory)
- 3 goal tùy chọn: G0 (0,6) · G1 (3,6) · G2 (6,0)

### 10.2. Hiển thị thông tin theo thời gian thực ✅

Tab **Mô phỏng** — cột phải (bảng THÔNG TIN):
- vị trí (row, col), hướng bay (NORTH/EAST/SOUTH/WEST)
- goal hiện tại, khoảng cách đến mục tiêu
- hành động vừa chọn, reward tức thời, tổng reward
- số bước, trạng thái gói hàng (ĐÃ LẤY HÀNG / CHƯA CÓ HÀNG)
- trạng thái episode (ĐANG CHẠY / THÀNH CÔNG / THẤT BẠI)
- thanh progress reward

### 10.3. Replay nhiều seed ✅

Tab **Replay** — chọn seed 0 đến 9, điều chỉnh delay từng bước, phát lại episode hoàn chỉnh.

### 10.4. So sánh thuật toán ✅

Tab **So sánh** — 3 bar chart đánh giá greedy:
- Success Rate (%)
- Avg Steps (±std)
- Collision Rate (%)

Tab **Learning Curves** — 2 biểu đồ so sánh reward MA và success rate MA, đường Target 85%.

Để so sánh observable vs hidden wind: vào tab Cài đặt → đổi Wind Mode → xem lại So sánh và Learning Curves.

### 10.5. Trực quan policy ✅

`dashboard/components/policy_view.py` có sẵn. Tích hợp thêm vào tab nếu cần hiển thị mũi tên policy trên từng ô.

---

## 11. Nội dung báo cáo chi tiết nhóm có thể dùng trực tiếp

# 11.1. Trang bìa

Gồm:

- tên trường
- tên môn học
- tên đề tài: **Drone giao hàng trong gió**
- tên nhóm
- danh sách thành viên
- giảng viên
- thời gian thực hiện

---

# 11.2. Tóm tắt báo cáo

Viết ngắn gọn 1 đoạn nêu:

- bài toán là gì
- vì sao có yếu tố khó do gió stochastic
- nhóm cài những agent nào
- kết quả chính là gì
- so sánh observable và hidden wind ra sao

---

# 11.3. Phát biểu bài toán

Phần này nên trả lời rõ:

### Agent là gì?

Agent là drone tự hành ra quyết định hành động trong lưới nhằm hoàn thành nhiệm vụ giao hàng.

### Môi trường là gì?

Môi trường là một gridworld 7x7 có:

- pickup point
- dropoff point
- vùng cấm bay
- gió đổi theo thời gian
- transition stochastic

### Mục tiêu dài hạn là gì?

Tối đa hóa tổng reward dài hạn bằng cách:

- giao hàng thành công
- tránh vùng cấm và va chạm
- giảm số bước di chuyển
- giữ policy ổn định dưới tác động của gió

---

# 11.4. Mô hình MDP

Phần này nên trình bày riêng từng thành phần.

## State

Mô tả 2 biến thể:

- observable: `(r, c, wind, has_package)`
- hidden: `(r, c, has_package)`

Phải nêu:

- ý nghĩa từng thành phần
- kích thước state space
- state nào là đủ thông tin, state nào thiếu thông tin

## Action

Mô tả tập action và cách mã hóa.

Nếu có `pick/drop`, phải nói rõ. Nếu pickup/dropoff tự động, phải nói rõ điều đó.

## Transition

Viết rõ trình tự cập nhật trong `step()`.

Ví dụ nên mô tả bằng pseudocode:

1. nhận action
2. tính vị trí sau action
3. áp dụng hiệu ứng gió
4. xử lý boundary/obstacle/no-fly
5. tính reward
6. kiểm tra terminal/truncated
7. cập nhật wind mới

## Reward

Nêu bảng reward và giải thích ý đồ của từng thành phần.

Ví dụ:

- `-1` để khuyến khích hoàn thành nhanh
- `-20` để răn đe đi vào vùng cấm
- `+50` để đặt ưu tiên lớn cho hoàn thành nhiệm vụ
- `-0.5` cho wait để cho phép chờ nhưng không quá hấp dẫn

## Terminal và truncated

Phân biệt rõ:

- terminal: hoàn thành dropoff đúng
- truncated: hết số bước tối đa

## Giả định Markov có hợp lý không?

Phải phân tích:

- với observable wind: hợp lý hơn vì state có biến gió
- với hidden wind: không hoàn toàn Markov vì cùng một `(r, c, has_package)` có thể dẫn đến động lực khác nhau tùy gió thực sự đang tồn tại

Đây là phần phân tích rất quan trọng của đề tài.

---

# 11.5. Thuật toán

## Random Agent

Mô tả:

- chọn action ngẫu nhiên đều trong action space
- dùng làm baseline thấp nhất

## Heuristic Agent

Mô tả luật tay, ví dụ:

- ưu tiên tiến gần pickup nếu chưa lấy hàng
- sau khi có hàng thì tiến gần dropoff
- tránh no-fly zone nếu có thể
- khi gió bất lợi có thể chọn wait hoặc rẽ hướng an toàn

Phải nói rõ heuristic có dùng thông tin `wind` hay không.

## Q-Learning

Phải trình bày:

- bảng Q
- công thức cập nhật
- epsilon-greedy
- learning rate `alpha`
- discount `gamma`

## SARSA (thuật toán thứ hai — đã cài)

SARSA là on-policy TD: cập nhật Q theo đúng hành động sẽ thực hiện ở bước tiếp theo.

Công thức:

\[
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[r_{t+1} + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t)\right]
\]

Trong đó `a_{t+1}` là hành động do epsilon-greedy chọn từ `s_{t+1}`, không phải `max`.

Điểm khác biệt so với Q-Learning:
- Q-Learning dùng `max_a Q(s_{t+1}, a)` — học về policy tốt nhất (off-policy).
- SARSA dùng `Q(s_{t+1}, a_{t+1})` với `a_{t+1}` là hành động thực tế — thận trọng hơn.
- Trong môi trường stochastic như gió, SARSA tránh overestimate ở những nơi nguy hiểm.

Cài đặt quan trọng: `_pending_action` state machine — agent lưu hành động tiếp theo giữa các bước để đảm bảo `a_{t+1}` được chọn nhất quán.

## Double Q-Learning (cũng đã cài, có trong dashboard)

- Dùng hai bảng `Q1`, `Q2`.
- Giảm overestimation bias của Q-Learning.
- Phù hợp khi transition stochastic.

**Trong dashboard**, biểu đồ So sánh mặc định dùng `COMPARE_ALGOS = [random, heuristic, q_learning, sarsa]`. Double Q-Learning vẫn có sẵn ở tab Mô phỏng và sweep pipeline.

## Epsilon schedule

Nên mô tả cụ thể:

- `epsilon_start`
- `epsilon_end`
- `epsilon_decay`

Ví dụ:

- bắt đầu 1.0
- giảm dần về 0.05 hoặc 0.01
- evaluation dùng 0

## Hyperparameters

Nên có bảng:

- learning rate `alpha`
- discount `gamma`
- epsilon start
- epsilon end
- epsilon decay
- số episode train
- max steps mỗi episode
- số seed

---

# 11.6. Kiểm thử môi trường

Phần này phải có test và mô tả ngắn từng test.

## Test boundary

- Drone ở mép lưới đi ra ngoài thì có bị giữ nguyên không.
- Reward có đúng không.

## Test invalid action

- Nếu có `pick/drop`, thử pick sai hoặc drop sai.
- Xác nhận penalty đúng.

## Test terminal state

- Khi dropoff đúng, `terminated=True`.
- Q target ở terminal không dùng bootstrap.

## Test seed

- Cùng seed phải tái tạo cùng chuỗi wind và quỹ đạo khi action sequence giống nhau.

## Test encoder/decoder

- `state_decoder(state_encoder(s)) == s`
- Mã hóa phải một-một trong state space đang xét.

## Test reward logic

- reward step thường
- reward vào vùng cấm
- reward pickup đúng
- reward dropoff đúng
- reward wait

## Test wind transition

- xác nhận phân phối chuyển gió đúng theo ma trận đã định
- hoặc kiểm tra bằng đếm mẫu gần đúng nếu dùng mô phỏng nhiều lần

---

# 11.7. Thiết kế thực nghiệm

## Số seed

Bắt buộc ít nhất **10 seed**.

Ví dụ:

- 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

## Same training budget

Các thuật toán phải được train với ngân sách tương đương:

- cùng số episode
- cùng max steps
- cùng số seed

## Evaluation mode

Tất cả agent học được phải đánh giá với:

- `epsilon = 0`

## Chỉ số báo cáo

Nên có tối thiểu:

- mean return ± std
- success rate ± std
- average steps ± std
- no-fly violation rate ± std
- collision/boundary penalty count ± std

## Biểu đồ nên có

- learning curve theo episode
- bar chart so sánh success rate giữa các agent
- bar chart so sánh số bước trung bình
- bar chart so sánh violation rate
- biểu đồ riêng cho observable vs hidden wind

---

# 11.8. Kết quả thực nghiệm

Nên tổ chức thành các mục sau:

## So sánh baseline

- Random Agent
- Heuristic Agent
- Q-Learning
- Double Q-Learning hoặc SARSA

## So sánh theo biến thể state

- observable wind
- hidden wind

## Bảng kết quả gợi ý

| Agent | State variant | Success rate | Avg return | Avg steps | Violation rate |
|------|------|------:|------:|------:|------:|
| Random | Observable | ... | ... | ... | ... |
| Heuristic | Observable | ... | ... | ... | ... |
| Q-Learning | Observable | ... | ... | ... | ... |
| Double Q | Observable | ... | ... | ... | ... |
| Q-Learning | Hidden | ... | ... | ... | ... |
| Double Q | Hidden | ... | ... | ... | ... |

Nên ghi theo dạng:

- `mean ± std`

Ví dụ:

- `84.2 ± 5.1 %`

---

# 11.9. Phân tích kết quả

Phần này không chỉ mô tả số liệu mà phải giải thích.

## Policy học được có hợp lý không?

Cần nhận xét:

- agent có đi vòng để tránh no-fly zone không
- agent có lợi dụng gió thuận không
- agent có chọn wait đúng lúc không

## Agent còn lỗi gì?

Ví dụ:

- đôi lúc đứng yên quá nhiều
- mắc kẹt gần vùng cấm
- quá nhạy với một số seed

## Reward có gây hành vi ngoài ý muốn không?

Đây là mục rất quan trọng. Ví dụ:

- reward wait quá nhẹ nên agent chờ quá nhiều
- reward step chưa đủ mạnh nên đường đi còn dài
- penalty vùng cấm chưa đủ mạnh nên agent chấp nhận vi phạm để rút ngắn đường

## Kết quả có ổn định giữa các seed không?

Phân tích dựa trên:

- độ lệch chuẩn
- hình dạng learning curve
- khác biệt giữa các seed

## Vì sao hidden wind kém hơn?

Phải liên hệ với lý thuyết:

- state thiếu thông tin
- môi trường thực sự có dynamics phụ thuộc gió
- agent học từ quan sát không đầy đủ nên giá trị Q bị trộn giữa nhiều tình huống khác nhau

## Double Q-Learning có giúp gì không?

Nếu dùng Double Q-Learning, nên phân tích:

- có giảm overestimation không
- có ổn định hơn Q-Learning thường không
- có tốt hơn rõ ràng ở môi trường stochastic không

---

# 11.10. Demo và tái lập

Phần này nên có:

- link video demo
- lệnh chạy train
- lệnh chạy evaluation
- lệnh chạy dashboard/demo
- mô tả file cấu hình chính
- link GitHub public của dự án

Lệnh cần thiết:

```bash
# Cài thư viện
pip install -r requirements.txt

# Mở dashboard (tự train inline)
streamlit run dashboard/app.py

# Hoặc train và evaluate riêng
python experiments/train.py --algo sarsa --wind-mode observable --seed 0
python experiments/evaluate.py --algo sarsa --wind-mode observable --seed 0
python experiments/sweep.py --config experiments/configs.yaml
```

Dashboard không cần pre-train — tự train trong bộ nhớ khi mở lần đầu.

---

# 11.11. Kết luận

Phần kết luận nên trả lời ngắn gọn:

- nhóm đã xây dựng được gì
- môi trường có đặc điểm gì đáng chú ý
- thuật toán nào tốt nhất
- quan sát về ảnh hưởng của việc ẩn/hiện biến gió
- hạn chế hiện tại và hướng cải thiện

---

## 12. Checklist nghiệm thu nhanh cho nhóm

Trước khi nộp, nên tự kiểm tra từng câu sau.

### 12.1. MDP

- State có đủ thông tin để ra quyết định không?
- Action có được định nghĩa rõ ràng không?
- Reward có khuyến khích đúng hành vi không?
- Terminal và truncated có tách riêng không?

### 12.2. Môi trường

- Có `reset(seed)` không?
- Có `step(action)` không?
- Có `render()` không?
- Có `state_encoder()` và `state_decoder()` không?
- Có test transition, reward, terminal, seed, encoder/decoder không?

### 12.3. Thuật toán

- Có Random Agent không?
- Có Heuristic Agent không?
- Có Q-Learning không?
- Có Double Q-Learning hoặc SARSA không?
- Có epsilon-greedy không?
- Evaluation có dùng `epsilon = 0` không?

### 12.4. Thực nghiệm

- Có ít nhất 10 seed không?
- Các agent có cùng training budget không?
- Có báo cáo `mean ± std` không?
- Có learning curve không?
- Có success rate không?
- Có average steps không?
- Có violation rate không?

### 12.5. Riêng cho đề tài drone

- Có hiển thị hướng gió hiện tại không?
- Có replay 3 seed khác nhau không?
- Có hiển thị đường bay và vùng cấm không?
- Có bảng so sánh observable và hidden wind không?
- Có giải thích vì sao hidden wind kém hơn không?

### 12.6. Demo và báo cáo

- Demo chạy được sau khi train không?
- Có trực quan policy không?
- Có hướng dẫn chạy lại không?
- Có link dự án public không?

---

## 13. Gợi ý cấu trúc thư mục báo cáo trong dự án

Nhóm có thể đặt tài liệu và hình theo cách sau:

```text
reports/
  figures/
    learning_curve_observable.png
    learning_curve_hidden.png
    policy_observable.png
    policy_hidden.png
    comparison_success_rate.png
  final_report.pdf
  report_outline.md
```

Tài liệu hiện tại có thể dùng như bản nháp ban đầu để phát triển thành `report_outline.md` hoặc làm khung cho `final_report.pdf`.

---

## 14. Những lỗi thường gặp cần tránh

### 14.1. Tính reward trước khi hoàn tất transition

Nếu gió làm lệch drone nhưng reward lại tính trước khi áp dụng gió thì logic rất khó giải thích. Nhóm nên chốt rõ thứ tự cập nhật và dùng nhất quán.

### 14.2. Không nói rõ gió là state hay biến ẩn

Đây là lỗi nghiêm trọng vì ảnh hưởng trực tiếp đến tính Markov và diễn giải kết quả.

### 14.3. Reward wait quá hấp dẫn

Nếu `wait` tốt hơn di chuyển trong nhiều tình huống thì agent có thể học đứng yên.

### 14.4. Không xử lý terminal đúng trong Q update

Ở terminal state, target chỉ là reward nhận được, không cộng phần bootstrap tương lai.

### 14.5. Chỉ chọn một seed đẹp để báo cáo

RL có phương sai cao. Báo cáo phải dùng nhiều seed và thống kê tổng hợp.

---

## 15. Kết luận ngắn cho riêng đề tài này

Đề tài Drone giao hàng trong gió là một đề tài phù hợp để thể hiện đầy đủ các yêu cầu cốt lõi của môn RL vì có:

- môi trường tự thiết kế rõ ràng
- transition stochastic do gió
- khả năng so sánh state đầy đủ và state thiếu thông tin
- baseline dễ xây dựng
- nhiều chỉ số để phân tích ngoài reward

Nếu nhóm làm tốt phần định nghĩa MDP, test môi trường, đánh giá 10 seed và so sánh observable với hidden wind, đây sẽ là một báo cáo rất mạnh cả về kỹ thuật lẫn phân tích.
