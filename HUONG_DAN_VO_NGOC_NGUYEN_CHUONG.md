# Hướng dẫn triển khai chi tiết cho Võ Ngọc Nguyên Chương

## Trạng thái hiện tại

Dashboard Streamlit 5 tab đã được xây dựng hoàn chỉnh tại `dashboard/app.py`. Chương tập trung vào:

- **Sử dụng và demo dashboard đã có**
- **Chọn cấu hình đẹp** để trình bày kết quả thuyết phục
- **Quay video demo**
- Bổ sung thêm nếu cần (policy map, so sánh observable/hidden)

## Vai trò chính

Võ Ngọc Nguyên Chương phụ trách phần **demo, giao diện, video trình bày**. Chương cần làm phần trình diễn theo hướng:

- thể hiện được **agent tốt nhất**
- hỗ trợ **trình bày kết quả đẹp và rõ**
- phối hợp với phần thực nghiệm để **chọn cấu hình mạnh nhất cho demo**
- tối ưu trải nghiệm người xem khi nghiệm thu

Nói rõ hơn, Chương sẽ là người biến kết quả kỹ thuật thành phần trình bày trực quan, thuyết phục và dễ ghi điểm.

---

## 1. Mục tiêu đầu ra

Phần của Chương phải tạo được 3 đầu ra:

### 1.1. Ứng dụng demo chạy được ✅ ĐÃ XONG

Dashboard `dashboard/app.py` đã có đầy đủ:

- map 7×7 với dark HUD theme
- drone bay lơ lửng (hover effect: bóng đổ + rotor glow + nhịp bồng bềnh)
- P = pickup (vàng), G = dropoff (xanh), ✕ = no-fly (đỏ)
- bảng THÔNG TIN: action, reward, tổng reward, has_package, steps, trạng thái
- chọn agent, goal (G0/G1/G2), bản đồ (Cố định/Medium), tốc độ
- thống kê nhanh: Episode / Thành công / Tỷ lệ %
- 5 tab: Mô phỏng · Learning Curves · So sánh · Replay · Cài đặt

Để chạy:

```bash
streamlit run dashboard/app.py
```

### 1.2. Trình bày kết quả đẹp ✅ ĐÃ XONG (một phần)

Đã có trong dashboard:
- Tab **Learning Curves**: reward MA + success rate MA cho 4 thuật toán, đường Target 85%
- Tab **So sánh**: 3 bar chart — Success Rate, Avg Steps (±std), Collision Rate

Còn cần bổ sung:
- So sánh observable vs hidden: vào Cài đặt → đổi Wind Mode → chụp ảnh / record 2 lần
- Policy view: `dashboard/components/policy_view.py` có sẵn, cần tích hợp vào tab Mô phỏng nếu muốn

### 1.3. Video demo hoàn chỉnh

Video cần cho thấy:

- nhóm hiểu bài toán
- agent học được thật
- transition stochastic do gió là yếu tố quan trọng
- observable tốt hơn hidden
- agent RL tốt hơn baseline

---

## 2. Trọng tâm mới của phần Chương

Ngoài demo, Chương cần hỗ trợ phần **tối ưu để kết quả trình diễn đẹp**. Điều này không có nghĩa là tự đổi bài toán hay sửa luật tùy tiện, mà là chọn đúng cấu hình để:

- policy nhìn hợp lý
- replay ổn định
- success rate đủ cao
- đường đi không quá rối
- giao diện thể hiện được chất lượng agent

Chương cần phối hợp với người làm thực nghiệm để chọn:

- agent tốt nhất đem đi demo
- seed đẹp nhưng vẫn trung thực
- cấu hình observable và hidden rõ chênh lệch
- tốc độ replay phù hợp

---

## 3. Những gì Chương cần làm thêm về tối ưu kết quả

## 3.1. Chọn agent để demo

Không nên demo tất cả agent với thời lượng như nhau. Nên chọn:

- Random để làm đối chứng xấu
- Heuristic để làm baseline trung bình
- RL agent tốt nhất để kết bài

Agent RL mạnh nhất hiện tại (theo thứ tự ưu tiên demo):

1. **SARSA** — on-policy, ổn định trong môi trường stochastic, là thuật toán thứ hai chính
2. **Q-Learning** — nếu SARSA kết quả tương đương, dùng Q-Learning để giải thích công thức dễ hơn
3. Double Q-Learning — có sẵn ở tab Mô phỏng, dùng nếu muốn nói thêm về overestimation

## 3.2. Chọn seed demo

Demo phải trung thực, nhưng cũng cần dễ nhìn. Do đó:

- không chọn seed tệ bất thường làm hỏng phần trình bày
- không chọn seed quá đẹp nhưng trái với trung bình chung
- nên chọn 3 seed đại diện: một tốt, một trung bình, một hơi nhiễu nhưng vẫn thành công

## 3.3. Chọn tốc độ replay

Nếu chạy quá nhanh, giảng viên không kịp thấy action và gió. Nếu quá chậm, demo lê thê.

Khuyến nghị:

- mỗi bước 250ms đến 500ms
- có tùy chọn tăng tốc x2 hoặc x4
- có chế độ step-by-step để giải thích một quỹ đạo cụ thể

## 3.4. Chọn chế độ hiển thị policy

Vì state có thể nhiều lớp theo `wind` và `has_package`, cần chọn cách hiển thị đủ rõ mà không rối:

- với observable: chọn từng lớp `wind`
- với hidden: hiển thị một policy map đơn giản hơn
- tách `has_package = 0` và `has_package = 1`

---

## 4. Thiết kế giao diện đẹp và dễ chấm

## 4.1. Bố cục khuyến nghị

Giao diện nên chia 3 cột hoặc 3 vùng chính.

### Cột trái: điều khiển

- chọn agent
- chọn wind mode
- chọn seed
- start
- pause
- reset
- replay
- step
- speed slider

### Cột giữa: bản đồ chính

- grid 7x7 lớn, dễ nhìn
- drone nổi bật
- pickup/dropoff rõ màu
- no-fly zone đỏ đậm
- đường bay vẽ rõ
- mũi tên gió hoặc icon gió hiện trên góc màn hình

### Cột phải: thông tin + kết quả

- state hiện tại
- action hiện tại
- reward tức thời
- cumulative reward
- step count
- success/fail
- bảng metric ngắn
- ảnh learning curve hoặc bảng so sánh

Đây là bố cục vừa đẹp vừa dễ thuyết trình vì mắt người xem luôn tập trung vào trung tâm là bản đồ.

---

## 5. Quy chuẩn màu sắc và hiển thị

Để giao diện đẹp, phải nhất quán màu sắc.

### Gợi ý màu

- nền grid: trắng hoặc xám rất nhạt
- drone: xanh dương nổi bật
- pickup: vàng
- dropoff: xanh lá
- no-fly zone: đỏ
- obstacle: xám đậm
- đường bay: tím hoặc xanh cyan
- ô hiện tại: thêm viền sáng

### Gợi ý kiểu chữ

- tiêu đề rõ, to vừa đủ
- thông tin metric căn cột thẳng hàng
- số liệu quan trọng dùng font đậm

### Gợi ý icon

- gió: `↑ ↓ ← →` hoặc icon mũi tên
- package: biểu tượng hộp hàng nhỏ
- thành công: màu xanh lá
- thất bại/vi phạm: màu đỏ cam

---

## 6. Thành phần bắt buộc của app demo

## 6.1. Bản đồ môi trường

Phải có:

- lưới 7x7
- vị trí drone hiện tại
- pickup point
- dropoff point
- no-fly zone
- obstacle nếu môi trường có dùng
- vết đường bay đã đi qua

## 6.2. Panel trạng thái hiện tại

Phải hiển thị:

- `row, col`
- `wind`
- `has_package`
- `action`
- `reward`
- `cumulative_reward`
- `step`
- `terminated`
- `truncated`

## 6.3. Panel cấu hình chạy

Phải có:

- chọn agent
- chọn `observable/hidden`
- chọn seed
- chọn tốc độ
- nút bắt đầu
- nút pause
- nút reset
- nút step by step

## 6.4. Panel kết quả nhanh

Nên có:

- success rate của agent đang chọn
- average steps
- violation rate
- average return

---

## 7. Replay bắt buộc dưới 3 seed

## 7.1. Mục tiêu

Thể hiện rõ stochasticity do gió nhưng vẫn cho thấy RL policy ổn định.

## 7.2. Cách làm tốt nhất

Chuẩn bị sẵn 3 replay:

- Seed A: quỹ đạo ngắn và sạch
- Seed B: có nhiễu gió nhưng vẫn thành công
- Seed C: quỹ đạo vòng hơn một chút để minh họa stochastic transition

## 7.3. Hai cách trình bày

### Cách 1: chạy lần lượt

Ưu điểm:

- dễ làm
- ít lỗi giao diện
- phù hợp khi quay video

### Cách 2: 3 panel song song

Ưu điểm:

- rất đẹp
- gây ấn tượng mạnh
- cho thấy cùng policy nhưng quỹ đạo khác nhau

Nhược điểm:

- khó làm hơn
- dễ rối nếu màn hình nhỏ

Nếu đủ thời gian, 3 panel song song là lựa chọn đẹp hơn cho demo cuối.

---

## 8. So sánh observable và hidden trong giao diện

Đây là phần rất đáng điểm vì bám sát yêu cầu đề tài.

## 8.1. Cách hiển thị nên làm

Một bảng nhỏ bên cạnh hoặc phía dưới gồm:

| Mode | Success rate | Avg steps | Violation rate |
|------|-------------:|----------:|---------------:|
| Observable | ... | ... | ... |
| Hidden | ... | ... | ... |

## 8.2. Điều cần nói khi demo

- observable tốt hơn vì state chứa wind
- hidden kém hơn vì agent thiếu thông tin để dự đoán lệch hướng
- đây là minh họa cho việc state không còn Markov đầy đủ

---

## 9. Trực quan policy đẹp và dễ hiểu

## 9.1. Policy map

Nên hiển thị action tốt nhất bằng mũi tên trên từng ô.

Ví dụ:

- `↑` đi lên
- `→` đi phải
- `↓` đi xuống
- `←` đi trái
- `•` hoặc `W` cho wait

## 9.2. Tách theo lớp state

Với đề tài này, policy không chỉ phụ thuộc vị trí mà còn phụ thuộc:

- `has_package`
- `wind` nếu observable

Do đó nên có lựa chọn:

- `has_package = 0 / 1`
- `wind = calm / north / east / west`

## 9.3. Cách đơn giản nhưng đẹp

Hiển thị 4 tab hoặc 4 nút:

- calm
- north
- east
- west

Mỗi tab hiện một policy map riêng.

---

## 10. Chương cần hỗ trợ tối ưu thuật toán theo góc nhìn demo

Phần tối ưu ở đây là **tối ưu cho chất lượng trình diễn và kết quả**, không phải thay đổi bản chất bài toán.

## 10.1. Những chỗ Chương cần góp ý với người train

- reward `wait` có quá hấp dẫn không
- policy có bị đứng yên nhiều không
- đường đi có quá ngoằn ngoèo không
- agent có thường lao vào no-fly zone không
- có seed nào replay đẹp và đại diện không

## 10.2. Những hướng tối ưu hợp lý

### Điều chỉnh reward nhẹ nếu cần

- tăng phạt no-fly nếu agent liều đi xuyên vùng cấm
- tăng phạt step nếu agent đi vòng quá nhiều
- giảm lợi ích của wait nếu agent đứng chờ quá lâu

### Điều chỉnh train budget

- tăng số episode nếu learning curve chưa hội tụ
- giảm epsilon chậm hơn nếu agent khám phá chưa đủ
- dùng Double Q nếu Q-Learning hay overestimate và policy kém ổn định

### Điều chỉnh demo seed

- chọn seed có hành vi đại diện
- tránh seed khiến replay bị quá dài, khó thuyết trình

---

## 11. Phần trình bày kết quả đẹp trong app

Ngoài chạy environment, app nên có một tab hoặc panel `Results` gồm:

- learning curve ảnh tĩnh hoặc chart
- bar chart success rate
- bar chart avg steps
- bar chart violation rate
- bảng observable vs hidden

### Tư duy trình bày

Người xem demo không cần thấy quá nhiều số. Chỉ cần thấy:

- agent nào tốt nhất
- khác nhau giữa observable và hidden
- RL tốt hơn baseline
- policy học được trông hợp lý

Do đó phần này cần **ít nhưng đắt**, không nhồi nhét quá nhiều biểu đồ nhỏ.

---

## 12. Kịch bản demo trực tiếp nên đi theo thứ tự này

## Bước 1: giới thiệu nhanh bài toán

Nói trong 20 đến 30 giây:

- drone giao hàng trên lưới 7x7
- có pickup, dropoff, no-fly zone
- gió làm transition stochastic

## Bước 2: chỉ giao diện

- map ở giữa
- panel điều khiển bên trái
- số liệu và kết quả bên phải

## Bước 3: chạy Random Agent

Mục tiêu:

- cho thấy baseline yếu
- đường đi xấu
- dễ vi phạm hoặc tốn nhiều bước

## Bước 4: chạy Heuristic Agent

Mục tiêu:

- khá hơn random
- có định hướng nhưng chưa thật ổn định

## Bước 5: chạy RL agent tốt nhất

Mục tiêu:

- chính là phần ăn điểm
- đường đi hợp lý
- tránh vùng cấm tốt hơn
- hoàn thành nhanh hơn

## Bước 6: replay 3 seed

Mục tiêu:

- cho thấy stochasticity
- cho thấy policy vẫn bền vững

## Bước 7: mở bảng observable vs hidden

Mục tiêu:

- chốt ý nghĩa khoa học của đề tài
- state thiếu wind làm giảm hiệu quả

---

## 13. Kịch bản video nên quay

Video dài 3 đến 5 phút là đẹp.

### Cảnh 1

Slide tiêu đề hoặc màn hình intro:

- tên đề tài
- tên nhóm
- mục tiêu

### Cảnh 2

Môi trường tĩnh:

- chỉ pickup
- dropoff
- no-fly zone
- giải thích gió

### Cảnh 3

Random Agent chạy ngắn

### Cảnh 4

Heuristic Agent chạy ngắn

### Cảnh 5

RL agent tốt nhất chạy đầy đủ

### Cảnh 6

Replay 3 seed

### Cảnh 7

Hiển thị bảng kết quả + biểu đồ ngắn

### Cảnh 8

Kết luận:

- agent tốt nhất là gì
- observable tốt hơn hidden thế nào
- bài học rút ra

---

## 14. Script nói gợi ý khi quay video

### Mở đầu

"Đề tài của nhóm là Drone giao hàng trong gió. Drone cần di chuyển trong lưới 7x7 để lấy hàng và giao đến đích. Thách thức chính là gió làm lệch hướng bay, khiến môi trường có transition stochastic."

### Khi chỉ giao diện

"Ở giữa là bản đồ môi trường. Drone được hiển thị bằng màu xanh dương, pickup màu vàng, dropoff màu xanh lá, vùng cấm bay màu đỏ. Bên phải là thông tin trạng thái, hành động, reward tức thời và kết quả tổng hợp."

### Khi chạy Random

"Random Agent chỉ chọn hành động ngẫu nhiên nên quỹ đạo không ổn định, thường tốn nhiều bước và dễ có vi phạm hơn."

### Khi chạy Heuristic

"Heuristic Agent đi theo luật tay nên có định hướng hơn, nhưng vẫn chưa xử lý tốt mọi nhiễu gió."

### Khi chạy RL

"Đây là agent học tăng cường sau huấn luyện. Có thể thấy agent chọn đường đi hợp lý hơn, tránh vùng cấm tốt hơn và hoàn thành nhiệm vụ ổn định hơn."

### Khi chiếu 3 seed

"Ba replay này dùng cùng policy nhưng seed khác nhau nên gió thay đổi theo thời gian. Điều này làm quỹ đạo khác nhau, nhưng policy tốt vẫn giữ được hiệu quả tương đối ổn định."

### Khi so sánh observable và hidden

"Khi agent quan sát được gió, kết quả tốt hơn rõ rệt. Khi ẩn biến wind, state thiếu thông tin nên quyết định kém chính xác hơn."

---

## 15. Công nghệ nên dùng cho giao diện

Nếu ưu tiên nhanh và đẹp, nên chọn một trong hai hướng:

### Hướng 1: Streamlit

Ưu điểm:

- nhanh làm
- dễ tạo layout đẹp
- dễ gắn ảnh biểu đồ
- phù hợp demo học thuật

Nhược điểm:

- animation từng bước không mượt bằng game loop

### Hướng 2: Pygame hoặc Tkinter canvas

Ưu điểm:

- animation tốt hơn
- replay trực quan hơn

Nhược điểm:

- tốn thời gian làm đẹp giao diện hơn

Nếu mục tiêu là **nhanh, đẹp, dễ demo**, Streamlit thường là lựa chọn hợp lý nhất.

---

## 16. Checklist công việc của Chương

**Đã hoàn thành trong dashboard:**
- [x] Chọn framework giao diện (Streamlit dark HUD)
- [x] Layout 3 vùng: điều khiển · bản đồ · thông tin
- [x] Grid 7×7 đẹp, dark theme
- [x] Drone bay lơ lửng (hover effect: bóng đổ + rotor glow)
- [x] Pickup P (vàng), dropoff G (xanh), no-fly ✕ (đỏ)
- [x] Hiển thị action, reward tức thời, cumulative reward, steps
- [x] Chọn agent (SARSA, Q-Learning, Double Q, Heuristic, Random)
- [x] Chọn goal (G0 / G1 / G2)
- [x] Chọn speed slider
- [x] Tab Replay — replay seed 0–9
- [x] Tab Learning Curves — đường cong 4 thuật toán
- [x] Tab So sánh — 3 bar chart

**Còn cần làm:**
- [ ] Chọn 3 seed đẹp để quay video (seed 0, 1, 2 thường tốt)
- [ ] Chạy với observable vs hidden, chụp ảnh/so sánh Tab So sánh
- [ ] Quay video demo hoàn chỉnh (3–5 phút)
- [ ] Kiểm tra tốc độ replay 250–400ms khi quay video
- [ ] Bổ sung policy view vào demo nếu cần (policy_view.py đã có)

---

## 17. Tiêu chí hoàn thành cuối cùng

Phần của Võ Ngọc Nguyên Chương được xem là hoàn thành khi:

- ứng dụng demo chạy ổn định bằng `streamlit run dashboard/app.py`
- giao diện dark HUD đẹp, drone bay lơ lửng rõ trên máy chiếu
- thể hiện được state, action, reward, đường bay và kết quả
- replay được 3 seed khác nhau (tab Replay)
- trình bày được sự khác nhau giữa observable và hidden (Tab Cài đặt → đổi Wind Mode → Tab So sánh)
- video demo 3–5 phút, ngắn gọn, mạch lạc
- nhìn vào video là thấy SARSA/Q-Learning đã học được policy tốt hơn Random/Heuristic
