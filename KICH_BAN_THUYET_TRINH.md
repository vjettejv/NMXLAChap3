# Kịch bản thuyết trình Fourier Lab — 9–10 phút

Lời trong dấu ngoặc kép có thể nói trực tiếp. Phần **Thao tác** dành cho người điều khiển demo. Mỗi lần thay tham số, dừng 2 giây để người nghe quan sát.

**Chuẩn bị:** Mở demo, Reset, chọn Cameraman và bật Chế độ trình chiếu. Dùng cùng một ảnh xuyên suốt. Không đọc hết công thức; không học thuộc số SNR hoặc thời gian chạy, hãy đọc kết quả thực tế.

## 1. Tổng quan — 55 giây

**Thao tác:** Chọn Tổng quan, chỉ ảnh gốc rồi phổ Fourier.

“Em xin chào thầy cô và các bạn. Nhóm em trình bày về tích chập và lọc ảnh trong miền tần số. Qua demo, em sẽ minh họa ba việc: làm mịn ảnh, loại nhiễu và phục hồi ảnh bị mờ.

Thông thường, chúng ta nhìn ảnh qua các điểm ảnh sáng tối. Fourier cho phép phân tích cùng ảnh đó thành những thành phần thay đổi chậm hoặc nhanh.

Một vùng nền khá đều thay đổi chậm, tương ứng tần số thấp. Những chỗ chuyển nhanh từ sáng sang tối, như mép người và máy ảnh, chứa tần số cao. Nhiễu cũng có thể chứa cao tần.

Trên phổ đã đưa tâm về giữa, gần tâm là thấp tần, xa tâm là cao tần. Điểm sáng trên phổ nghĩa là thành phần tần số đó có biên độ lớn; không phải vị trí sáng tương ứng trên ảnh gốc.”

**Chuyển ý:** “Vậy chúng ta xử lý ảnh thông qua phổ như thế nào?”

## 2. Convolution Theorem — 50 giây

**Thao tác:** Chọn Convolution Theorem, bật Minh họa từng bước. Chỉ ảnh, kernel, phổ và kết quả.

“Kernel là một ma trận nhỏ quy định cách kết hợp một điểm ảnh với các điểm xung quanh. Thực hiện phép kết hợp này trên ảnh là tích chập trong miền không gian.

Định lý tích chập cho phép tính tương đương bằng cách: biến đổi ảnh và kernel sang miền tần số, nhân hai phổ, rồi biến đổi ngược để nhận ảnh kết quả.

Các ô trên màn hình giúp theo dõi từng bước. Demo cũng đối chiếu hai cách tính và hiển thị sai số. Khi xử lý biên nhất quán, hai kết quả phải gần như giống nhau.”

**Chuyển ý:** “Em dùng Gaussian để minh họa tác động của kernel rõ hơn.”

## 3. Gaussian Blur — 45 giây

**Thao tác:** Chọn Gaussian Blur, kernel 51, tăng sigma từ 2 lên 6. Chỉ ảnh kết quả và phổ kernel; xoay đồ thị 3D nếu thuận tiện.

“Gaussian có trọng số lớn ở tâm và giảm dần ra xung quanh, giống hình một ngọn đồi.

Khi tăng sigma, các điểm ảnh được lấy trung bình trên vùng rộng hơn nên ảnh mờ hơn. Mọi người nhìn mép người và máy ảnh sẽ thấy chi tiết giảm đi.

Trong miền tần số, Gaussian giữ mạnh thấp tần và giảm cao tần. Vì vậy, làm mờ Gaussian là một dạng lọc thông thấp.”

## 4. HPF — Bộ lọc thông cao — 45 giây

**Thao tác:** Chọn HPF, đổi cutoff từ 10 lên 50. Bật Tăng cường biên trên ảnh gốc.

“Bộ lọc thông cao loại vùng thấp tần ở tâm và giữ cao tần bên ngoài. Trong mặt nạ này, vùng tối bị loại, vùng sáng được giữ.

Kết quả làm nổi những chỗ thay đổi nhanh, chẳng hạn đường biên, tức ranh giới giữa các vùng ảnh khác nhau. Khi cộng kết quả này vào ảnh gốc, cạnh có thể rõ hơn.

Tuy nhiên, tăng cutoff không có nghĩa luôn tốt hơn, vì ta đang loại thêm thông tin. Nhiễu cũng có thể nổi bật. Màu đỏ và lam trong kết quả HPF biểu diễn giá trị dương, âm, không phải màu thật của ảnh.”

## 5. LPF và khử nhiễu bằng FFT — 65 giây

**Thao tác:** Chọn LPF → Làm mịn. Với Ideal LPF, đổi cutoff từ 10 lên 60, sau đó chọn Gaussian LPF.

“Thông thấp làm ngược lại: giữ vùng gần tâm và giảm cao tần. Với bộ lọc lý tưởng, ngưỡng nhỏ giữ ít chi tiết nên ảnh mờ hơn. Tăng ngưỡng cho phép nhiều chi tiết đi qua.

Gaussian giảm dần thay vì cắt đột ngột, nên chuyển tiếp mềm hơn.”

**Thao tác:** Mở tab Khử nhiễu bằng FFT. Giữ độ lệch chuẩn nhiễu 0,06; đổi ngưỡng giữ lại từ 60 xuống 25.

“Ở đây em thêm nhiễu Gaussian rồi lọc trong miền tần số. Khi giảm ngưỡng, hạt nhiễu nhỏ có thể bớt rõ, nhưng mép vật thể và chi tiết cũng bị mờ.

Đó là sự đánh đổi giữa giảm nhiễu và giữ nội dung thật. Nhiễu Gaussian trải trên nhiều tần số nên không thể loại sạch chỉ bằng cách cắt cao tần.”

## 6. BPF — Bộ lọc thông dải — 35 giây

**Thao tác:** Chọn BPF, sigma 1 = 1,5 và sigma 2 = 4. Chỉ hai ảnh Gaussian rồi kết quả DoG.

“Thông dải nhấn mạnh một khoảng tần số ở giữa. Demo dùng DoG, tức lấy hiệu hai ảnh làm mờ Gaussian ở hai mức khác nhau.

Những cấu trúc khác nhau giữa hai mức làm mờ sẽ nổi bật. Thay đổi hai sigma giúp chọn thang chi tiết muốn quan sát. Ta cần giữ sigma thứ nhất nhỏ hơn sigma thứ hai.”

## 7. Notch Filter — Loại nhiễu sọc — 65 giây

**Thao tác:** Chọn Notch Filter, giữ mặc định, nhấn Thêm nhiễu tuần hoàn. Chỉ sọc trên ảnh và cặp đỉnh trong phổ.

“Với nhiễu lặp lại thành sọc, chúng ta có một cách chọn lọc hơn. Sóng sin tạo một cặp đỉnh đối xứng trên phổ. Thay vì bỏ cả vùng cao tần, em chỉ loại hai vùng nhỏ quanh cặp đỉnh gây nhiễu.”

**Thao tác:** Chọn dấu tròn ứng với nhiễu. Với mặc định là (32, 12) và (−32, −12). Giữ bán kính 2, nhấn Áp dụng Notch Filter, kéo thanh so sánh.

“Mọi người nhìn vùng nền sẽ thấy sọc giảm sau lọc. Notch phù hợp ở đây vì nhiễu tập trung tại những tần số xác định.

Nếu chọn sai đỉnh hoặc bán kính quá rộng, ta có thể xóa cả thông tin thật. Không phải mọi điểm sáng trên phổ đều là nhiễu.”

**Dự phòng:** Nếu khó click đúng, chọn Nhập tọa độ, nhập u = 32, v = 12 với thông số nhiễu mặc định.

## 8. Image Restoration — Inverse và Wiener — 95 giây

**Thao tác:** Chọn Image Restoration → Inverse Filter. Giữ sigma 2, kernel 21, epsilon mặc định; chưa bật nhiễu.

“Tiếp theo là phục hồi ảnh bị mờ. Trong thí nghiệm này, em chủ động làm mờ nên biết kernel gây mờ. Em cũng có ảnh gốc để kiểm tra kết quả phục hồi.

Inverse Filter cố đảo ngược quá trình gây mờ bằng cách chia phổ ảnh quan sát cho đáp ứng của bộ lọc. Khi ít nhiễu và mô hình phù hợp, cách này có thể lấy lại chi tiết.”

**Thao tác:** Bật Thêm nhiễu Gaussian, đặt độ lệch chuẩn 0,015. Nếu cần, giảm số mũ epsilon từ −3 xuống −5 để thấy tính không ổn định.

“Khi có nhiễu, phép chia cho những giá trị rất nhỏ có thể khuếch đại nhiễu mạnh. Epsilon giúp ổn định phép tính nhưng không giải quyết hoàn toàn vấn đề.”

**Thao tác:** Sang Wiener Filter. Giữ sigma 2, kernel 21, mức nhiễu 0,015 để so sánh cùng điều kiện. Kéo Mờ / Phục hồi rồi Gốc / Phục hồi.

“Wiener cân bằng khử mờ với hạn chế khuếch đại nhiễu, nên thường ổn định hơn phép nghịch đảo trực tiếp khi ảnh có nhiễu.

Tuy vậy, Wiener không đảm bảo lấy lại toàn bộ chi tiết. Kết quả vẫn phụ thuộc mô hình và tham số. Ở đây, tham số mặc định còn sử dụng thông tin ảnh sạch trong thí nghiệm; với ảnh thực, thông tin đó thường phải được ước lượng.”

## 9. So sánh Convolution — 40 giây

**Thao tác:** Chọn So sánh Convolution, ảnh 96 px, kernel 11, lặp 10 lần, chạy benchmark.

“Em so sánh tích chập trực tiếp với tích chập dùng FFT trên cùng ảnh, cùng kernel và cùng cách xử lý biên.

Thời gian đang hiển thị là phép đo thật trên máy. Sai số cho biết hai đầu ra khác nhau bao nhiêu. Theo kết quả này, phương pháp nhanh hơn là…”

**Đọc tên phương pháp theo kết quả thực tế, rồi nói tiếp:**

“FFT không luôn nhanh hơn. Với ảnh hoặc kernel nhỏ, chi phí biến đổi có thể lớn hơn lợi ích. Khi bài toán lớn hơn, FFT thường có lợi thế.”

## 10. Tổng kết — 30 giây

**Thao tác:** Chọn Tổng kết, chỉ bảng phương pháp.

“Mỗi vấn đề cần cách lọc phù hợp: LPF để làm mịn, HPF để nhấn biên, BPF để chọn một dải chi tiết và Notch để xử lý nhiễu tuần hoàn.

Khi biết mô hình gây mờ, có thể dùng Inverse hoặc Wiener, nhưng phải xét đến nhiễu. Điều quan trọng là quan sát cả ảnh lẫn phổ, chọn tham số và kiểm tra sự đánh đổi giữa giảm nhiễu với giữ chi tiết.

Phần trình bày của nhóm em đến đây kết thúc. Em cảm ơn thầy cô và các bạn.”

## Phần nâng cao tùy chọn — thêm 30–45 giây

**Thao tác:** Tắt Chế độ trình chiếu → Image Restoration → Wiener Filter → Thiết lập khôi phục → Unsupervised Wiener · scikit-image → Chạy Unsupervised Wiener.

“Ngoài Wiener theo công thức với K, demo có Unsupervised Wiener để ước lượng tham số từ ảnh quan sát, giảm việc chọn tham số thủ công. Tuy vậy, phương pháp trong demo vẫn được cung cấp kernel gây mờ, nên không phải tự tìm được mọi nguyên nhân làm hỏng ảnh.”

## Câu hỏi thường gặp

| Câu hỏi | Trả lời ngắn |
|---|---|
| Đường biên là gì? | Nơi mức sáng hoặc màu thay đổi rõ, như ranh giới người với nền; không chỉ là viền ngoài ảnh. |
| Thấp tần có phải vùng tối không? | Không. Tần số nói về tốc độ thay đổi giữa các điểm ảnh, không phải bản thân sáng hoặc tối. |
| Điểm sáng trên phổ là gì? | Thành phần tần số có biên độ lớn, không phải vị trí điểm sáng trên ảnh gốc. |
| FFT và Fourier khác nhau thế nào? | DFT là phép biến đổi Fourier rời rạc; FFT là thuật toán tính DFT hiệu quả. IFFT biến đổi ngược. |
| SNR cao nghĩa là gì? | Theo công thức demo, đầu ra gần ảnh gốc tham chiếu hơn. Không dùng nó để kết luận HPF tìm biên tốt hơn. |
| Vì sao Notch loại hai đỉnh? | Phổ của ảnh thực có tính đối xứng liên hợp. Lọc theo cặp duy trì tính chất đó để kết quả biến đổi ngược là ảnh thực. |
| Vì sao có viền gợn sau lọc? | Cắt tần số đột ngột có thể gây dao động gần biên, gọi là ringing. |
| Vì sao Wiener vẫn mờ? | Khử mờ phải cân bằng với giảm nhiễu. Điều hòa mạnh có thể làm mất chi tiết; thông tin suy giảm mạnh khó lấy lại. |
| CLAHE có ở demo này không? | Không. Đây là demo tích chập và lọc miền tần số; CLAHE là kỹ thuật tăng tương phản cục bộ, thuộc phạm vi khác. |

**Nếu chỉ có 7 phút:** Rút ngắn Gaussian, BPF và benchmark; vẫn giữ phần khử nhiễu FFT, Notch và Inverse/Wiener. Bỏ phần nâng cao tùy chọn.
