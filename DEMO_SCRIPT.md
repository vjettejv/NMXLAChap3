# Kịch bản demo Fourier Lab · 7–10 phút

## 1. Tổng quan · 45 giây

**Thao tác:** Trang Tổng quan, bật Chế độ trình chiếu.

“Nhóm em trình bày tích chập và lọc ảnh trong miền tần số. Bên trái là ảnh chúng ta
nhìn thấy, bên phải là phổ Fourier của cùng ảnh đó. Tâm phổ chứa tần số thấp,
liên quan đến các vùng thay đổi chậm. Xa tâm là tần số cao, liên quan tới cạnh,
chi tiết và cả nhiễu. Độ sáng trong phổ biểu diễn biên độ của thành phần tần số.”

## 2. Định lý tích chập · 1 phút

**Thao tác:** Convolution Theorem → Minh họa từng bước.

“Tích chập dùng kernel để kết hợp các pixel lân cận. Định lý tích chập cho phép
thực hiện thao tác tương đương bằng cách biến đổi cả ảnh và kernel sang miền tần số,
nhân hai phổ rồi biến đổi ngược. Sáu ô cho thấy ảnh, kernel, kết quả và các phổ tương ứng.”

**Thao tác:** Đổi sigma, giữ nguyên kernel.

“Kết quả thay đổi ngay khi tham số đổi. Demo zero-pad để tránh nhầm tích chập vòng
với tích chập tuyến tính; sai khác với fftconvolve được hiển thị bên dưới.”

## 3. Gaussian Blur · 1 phút

**Thao tác:** Kernel 51, sigma từ 2 lên 6; xem phổ 3D.

“Gaussian có trọng số mạnh ở tâm. Trong miền tần số, nó ưu tiên thấp tần và giảm
cao tần. Sigma không gian tăng làm ảnh mờ hơn, trong khi vùng tần số được giữ mạnh
hẹp lại. Gaussian vì vậy là một bộ lọc thông thấp.”

## 4. HPF, LPF và BPF · 2 phút

**HPF:** Đổi cutoff từ 10 lên 50; bật tăng cường biên.

“Vùng tối của mask bị loại. Khi loại thêm vùng trung tâm, ảnh mất thông tin nền,
các biên nổi bật tương đối. Cao tần cũng có thể là nhiễu, nên HPF không chỉ giữ
thông tin hữu ích. Đồ thị SNR đo độ gần ảnh gốc, không chấm chất lượng đường biên.”

**LPF:** Đổi cutoff từ 10 lên 60; chọn Gaussian LPF. Mở tab Khử nhiễu bằng FFT.

“LPF làm ngược lại: giữ thấp tần. Ngưỡng nhỏ làm ảnh mờ; tăng ngưỡng trả lại chi tiết.
Khi dùng để khử nhiễu, chúng ta phải đánh đổi vì chi tiết thật cũng có thể nằm ở cao tần.”

**BPF:** Sigma 1 = 1.5, Sigma 2 = 4.

“DoG lấy hiệu hai mức làm mờ để nhấn một dải cấu trúc trung gian. Kết quả có cả giá trị
dương và âm nên được hiển thị bằng hai màu; đây không phải màu nguyên bản của ảnh.”

## 5. Notch Filter · 1–2 phút

**Thao tác:** Thêm nhiễu tuần hoàn. Chỉ cặp đỉnh đối xứng, click dấu tròn, Áp dụng Notch.

“Sọc sin tạo một cặp đỉnh nổi bật trong phổ. Thay vì loại toàn bộ cao tần, ta loại
chọn lọc hai vùng nhỏ này. Sau IFFT, sọc giảm đi. Nhưng nếu notch quá rộng hoặc chọn
sai đỉnh, thông tin thật cũng bị mất. Không phải mọi đỉnh sáng đều là nhiễu.”

**Thao tác:** Kéo trước/sau, tăng bán kính từ 2 lên 8 để quan sát đánh đổi.

## 6. Inverse và Wiener · 1–2 phút

**Thao tác:** Image Restoration → Inverse; thử không nhiễu rồi bật nhiễu.

“Khôi phục ảnh cần mô hình gây mờ. Khi biết H, phép nghịch đảo chia phổ quan sát
cho H. Epsilon giúp tránh chia cho 0 nhưng không loại hết rủi ro khuếch đại nhiễu.
Khi H rất nhỏ, một lượng nhiễu nhỏ cũng có thể làm kết quả sai lệch lớn.”

**Thao tác:** Chuyển tab Wiener, kéo Mờ/Phục hồi.

“Wiener thêm thành phần điều hòa để cân bằng khử mờ và hạn chế nhiễu. Nó thường
ổn định hơn phép chia trực tiếp trong trường hợp có nhiễu, nhưng kết quả vẫn phụ
thuộc kernel và tham số. Đây là thí nghiệm tổng hợp với mô hình gây mờ đã biết.”

## 7. Benchmark và kết luận · 1 phút

**Thao tác:** Benchmark, ảnh 96 px, kernel 11, 10 lần → Run Benchmark.

“Hai cách dùng cùng ảnh, cùng kernel và cùng điều kiện biên. Đầu ra gần như giống
nhau, còn thời gian là phép đo thật trên máy hiện tại. FFT không luôn nhanh hơn;
ưu thế phụ thuộc kích thước ảnh, kernel và chi phí biến đổi.”

**Thao tác:** Tổng kết.

“Muốn làm mịn: LPF. Muốn nhấn biên: HPF. Muốn chọn một thang cấu trúc: BPF.
Nhiễu tuần hoàn: Notch. Khi biết mô hình gây mờ, cân nhắc Inverse hoặc Wiener tùy
mức nhiễu. Quan sát phổ và chọn tham số phù hợp là bước quan trọng nhất.”

Không đọc thuộc số liệu. Dừng 2–3 giây sau mỗi thao tác để người nghe quan sát.
