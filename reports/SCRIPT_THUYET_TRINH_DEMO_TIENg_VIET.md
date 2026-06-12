# SCRIPT THUYẾT TRÌNH DEMO DỰ ÁN
# DRONE GIAO HÀNG TRONG GIÓ

## 1. Mở đầu rất ngắn
Xin chào thầy/cô và các bạn.
Nhóm em xin trình bày đề tài **Drone giao hàng trong môi trường có gió** bằng phương pháp **học tăng cường - Reinforcement Learning**.

Mục tiêu của bài toán là huấn luyện một drone tự học cách:
- đi từ vị trí xuất phát,
- lấy hàng,
- né vùng cấm bay,
- vượt ảnh hưởng của gió,
- và giao hàng tới đích với phần thưởng cao nhất.

---

## 2. Nói bài toán bằng ngôn ngữ rất dễ hiểu
Có thể hiểu đơn giản thế này:

Drone giống như một thiết bị bay giao hàng trong mê cung.
Mỗi bước bay đều tốn chi phí.
Nếu bay vào vùng cấm thì bị phạt nặng.
Nếu lấy được hàng thì được thưởng.
Nếu giao hàng thành công thì được thưởng lớn nhất.

Khó khăn của bài toán là:
- môi trường có gió,
- gió có thể đẩy drone lệch khỏi hướng mong muốn,
- nên drone không chỉ cần đi ngắn, mà còn phải đi an toàn và ổn định.

---

## 3. Vì sao nhóm chọn Reinforcement Learning
Nhóm em chọn Reinforcement Learning vì đây là dạng bài toán mà agent phải tự học qua thử sai.

Tức là:
- lúc đầu agent đi rất kém,
- sau nhiều lần thử,
- agent sẽ học được đường bay nào tốt,
- đường bay nào nguy hiểm,
- và dần dần tối ưu chiến lược giao hàng.

Đây là điểm phù hợp nhất với bài toán drone hoạt động trong môi trường có yếu tố ngẫu nhiên như gió.

---

## 4. Giới thiệu nhanh các agent
Trong đề tài, nhóm em so sánh 4 agent chính:

### Random Agent
Agent này chọn hành động ngẫu nhiên.
Dùng làm mốc baseline thấp nhất.

### Heuristic Agent
Agent này đi theo luật đơn giản, ví dụ cố gắng tiến gần mục tiêu hơn.
Nó tốt hơn random nhưng vẫn không thực sự học từ dữ liệu.

### Q-Learning
Đây là thuật toán học tăng cường off-policy cơ bản.
Agent cập nhật giá trị Q theo công thức TD error, dùng max Q của trạng thái tiếp theo.

### SARSA
Đây là thuật toán on-policy — phiên bản "thực dụng" hơn Q-Learning.
Thay vì dùng giá trị tốt nhất có thể ở bước tiếp theo, SARSA dùng đúng hành động mà agent thực sự sẽ chọn.
Phù hợp với môi trường stochastic vì nó tính đến hành vi thực của policy hiện tại.

---

## 5. Giải thích môi trường rất trực quan
Môi trường của nhóm em là lưới **7 x 7**.

Trong đó có:
- điểm xuất phát của drone (góc trái dưới),
- điểm lấy hàng (P - màu vàng),
- điểm giao hàng (G - màu xanh lá),
- các ô cấm bay (✕ - màu đỏ),
- và trạng thái gió Markov thay đổi theo thời gian.

Drone có 5 hành động:
- đi lên (NORTH ↑),
- đi phải (EAST →),
- đi xuống (SOUTH ↓),
- đi trái (WEST ←),
- hoặc đứng yên (STOP).

Drone được hiển thị **đang bay lơ lửng phía trên lưới** với bóng đổ bên dưới và vòng sáng rotor, giúp phân biệt rõ đây là thiết bị bay chứ không phải xe mặt đất.

Mỗi lần bay sẽ bị trừ điểm nhẹ để khuyến khích tìm đường ngắn.
Bay vào vùng cấm sẽ bị phạt nặng.
Lấy được hàng sẽ được cộng điểm.
Giao hàng thành công sẽ được cộng điểm lớn và kết thúc episode.

---

## 6. Giải thích wind observable và hidden
Nhóm em xét 2 tình huống:

### Observable wind
Drone nhìn thấy trạng thái gió hiện tại.
Tức là trước khi hành động, nó biết gió đang như thế nào.

### Hidden wind
Drone không nhìn thấy gió.
Nó chỉ thấy vị trí của mình và trạng thái mang hàng.

Ý nghĩa của phần này là để kiểm tra xem:
**nếu agent có nhiều thông tin hơn thì học có tốt hơn không**.

Kết quả luôn cho thấy observable tốt hơn hidden vì state đầy đủ Markov hơn.

---

## 7. Bắt đầu demo dashboard
Bây giờ em xin demo giao diện trực quan của hệ thống.

Dashboard có 5 tab chính ở phía trên:
- **Mô phỏng** — chạy agent từng bước
- **Learning Curves** — đường cong học tập
- **So sánh** — bar chart so sánh 4 thuật toán
- **Replay** — phát lại episode hoàn chỉnh
- **Cài đặt** — thay đổi tham số

---

## 8. Demo tab Mô phỏng
Ở tab **Mô phỏng**, ta có thể xem drone chạy trực tiếp trên lưới.

Cột trái là bảng điều khiển:
- Chọn thuật toán (SARSA, Q-Learning, …).
- Chọn Goal: G0, G1, G2 — vị trí đích khác nhau.
- Chọn bản đồ: Cố định hoặc Medium (vùng cấm ngẫu nhiên).
- Điều chỉnh tốc độ auto.
- Các nút: Chạy thuật toán · Bước tiếp · Dừng · Episode mới.

Khi bấm **Chạy thuật toán**:
- drone bắt đầu từ vị trí xuất phát,
- bay lơ lửng với hiệu ứng bồng bềnh (có thể thấy drone nhịp nhẹ theo bước),
- di chuyển để lấy hàng P,
- tránh vùng cấm ✕,
- rồi giao đến đích G.

Cột phải (THÔNG TIN) hiển thị:
- vị trí hiện tại, hướng bay, goal, khoảng cách đến mục tiêu,
- hành động vừa chọn, reward tức thời, tổng reward,
- số bước, trạng thái gói hàng,
- thanh progress reward episode.

Phía dưới điều khiển có Thống kê nhanh: Episode / Thành công / Tỷ lệ %.

Khi demo, có thể nói câu này:

**"Ở đây ta không chỉ nhìn drone có đến đích hay không, mà còn nhìn được nó bay như thế nào — hành động, phần thưởng, và khoảng cách đến mục tiêu từng bước."**

---

## 9. Demo tab Learning Curves
Tiếp theo là tab **Learning Curves**.

Tab này cho thấy quá trình học của 4 thuật toán qua các episode:
- Biểu đồ trái: Reward trung bình trượt (MA).
- Biểu đồ phải: Success rate (%) với đường Target 85% màu đỏ.

Khi trình bày, có thể nói:

**"Nhìn vào đây, ta thấy SARSA và Q-Learning học dần lên và vượt qua mốc 85% thành công, trong khi Random và Heuristic không có xu hướng cải thiện."**

---

## 10. Demo tab So sánh
Tiếp theo là tab **So sánh**.

Ở đây có 3 bar chart:
- **Success Rate (%)** — thuật toán nào giao hàng thành công nhiều nhất.
- **Avg Steps (±std)** — thuật toán nào đi ngắn hơn (có error bar).
- **Collision Rate (%)** — thuật toán nào an toàn hơn.

Khi trình bày, có thể nói:

**"Nhìn vào bảng này, ta thấy SARSA và Q-Learning vượt trội so với Random và Heuristic về mọi chỉ số, đặc biệt trong chế độ observable."**

---

## 11. Demo tab Replay
Tab **Replay** cho phép phát lại toàn bộ một episode với seed tùy chọn.

Chọn seed 0, 1, 2 lần lượt để cho thấy:
- cùng policy nhưng quỹ đạo bay khác nhau do gió stochastic,
- policy vẫn thành công dù bị gió đẩy.

Khi demo, có thể nói:

**"Ba replay này dùng cùng policy nhưng gió khác nhau theo seed. Quỹ đạo bay khác nhau nhưng drone vẫn giao hàng thành công — đây là bằng chứng policy ổn định dưới stochastic transition."**

---

## 12. Nêu kết quả chính thật gọn
Kết quả chính mà nhóm em muốn nhấn mạnh là:

- Random gần như không ổn định và chỉ mang tính đối chứng.
- Heuristic khá hơn random nhưng vẫn bị giới hạn vì không tự học tối ưu.
- Q-Learning học được policy rõ ràng và cho kết quả tốt.
- SARSA — thuật toán on-policy — cho kết quả tương đương hoặc tốt hơn trong môi trường stochastic.
- Khi agent quan sát được gió, kết quả tốt hơn rõ rệt so với khi không quan sát được.

---

## 13. Nói về khó khăn và điểm tối ưu
Khó khăn lớn nhất của bài toán là yếu tố gió làm môi trường trở nên ngẫu nhiên.
Cùng một hành động nhưng kết quả không phải lúc nào cũng giống nhau.

Nhóm em đã tối ưu:
- số episode train và tốc độ giảm epsilon,
- chọn SARSA thay Double Q-Learning cho phần so sánh chính vì phù hợp với môi trường on-policy,
- giao diện trực quan với drone bay lơ lửng giúp người xem hình dung rõ đây là thiết bị bay.

---

## 14. Kết luận cuối bài
Tóm lại, đề tài đã xây dựng được:
- một môi trường drone giao hàng có gió Markov stochastic,
- 5 agent từ baseline đến RL: Random, Heuristic, Q-Learning, SARSA, Double Q-Learning,
- pipeline train và evaluate nhiều seed,
- cùng dashboard 5 tab trực quan để demo từng bước, so sánh thuật toán và replay.

Kết quả cho thấy Reinforcement Learning, đặc biệt là SARSA và Q-Learning, học được chiến lược giao hàng tốt hơn rõ rệt so với các baseline, và observable wind cho phép agent học hiệu quả hơn hidden wind.

---

## 15. Câu chốt khi kết thúc demo
Phần trình bày của nhóm em đến đây là hết.
Xin cảm ơn thầy/cô và các bạn đã lắng nghe.

---

## 16. Mẹo nói khi demo để dễ ăn điểm
- Nói chậm, ngắn, từng ý một.
- Không đọc nguyên văn mọi dòng trên màn hình.
- Mỗi tab chỉ cần nói đúng ý nghĩa chính.
- Khi drone bay thành công, nhấn mạnh: **agent đã học được policy hiệu quả trong môi trường có gió**.
- Khi xem So sánh, nhấn mạnh: **SARSA và Q-Learning tốt hơn baseline, observable tốt hơn hidden**.
- Chỉ vào drone trên màn hình: **"Drone hiển thị đang bay lơ lửng — bóng đổ bên dưới cho thấy đây là thiết bị bay, không phải xe mặt đất."**

---

## 17. Phiên bản cực ngắn 1 phút nếu bị hỏi nhanh
Đây là bài toán drone giao hàng trong môi trường có gió stochastic.
Nhóm em mô hình hóa dưới dạng MDP và dùng Reinforcement Learning để agent tự học cách bay, lấy hàng, tránh vùng cấm và giao hàng thành công.

Nhóm em cài 5 agent: Random, Heuristic, Q-Learning, SARSA và Double Q-Learning.
Kết quả cho thấy SARSA và Q-Learning học tốt hơn rõ rệt, đặc biệt khi agent quan sát được trạng thái gió.

Dashboard Streamlit 5 tab cho phép chạy từng bước, xem learning curve, so sánh bar chart, replay nhiều seed và điều chỉnh tham số — tất cả train inline trong bộ nhớ, không cần pre-train.
