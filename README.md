# Fourier Lab · Nhóm 1 – 74DCTT24

**Tích chập và lọc ảnh trong miền tần số: Biến đổi Fourier và các kỹ thuật lọc**

Ứng dụng Streamlit khám phá xử lý ảnh, với sidebar tối, nội dung sáng,
ảnh và phổ đồng bộ, tham số trực tiếp, hoạt cảnh DFT → nhân phổ → IDFT,
Notch tương tác, Inverse/Wiener và benchmark thực tế.

## Cài đặt và chạy trên Windows

### 1. Chuẩn bị

- Cài **Python 3.13** từ [python.org](https://www.python.org/downloads/). Khi cài, tích **Add python.exe to PATH**. Dự án được kiểm tra với Python 3.13.
- Cài [Git](https://git-scm.com/downloads) để tải mã nguồn. Có thể thay bằng **Code → Download ZIP** trên GitHub rồi giải nén.
- Cần mạng để tải mã nguồn và thư viện lần đầu.

### 2. Tải dự án

Mở PowerShell, chạy từng dòng:

```powershell
git clone https://github.com/vjettejv/NMXLAChap3.git
cd NMXLAChap3
```

Nếu tải ZIP: mở thư mục đã giải nén chứa `app.py`, nhấp phải vào vùng trống → **Open in Terminal**. Tất cả lệnh bên dưới phải chạy trong thư mục này.

### 3. Cài thư viện — chỉ làm lần đầu

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

`.venv` là môi trường Python riêng của dự án. Không cần kích hoạt môi trường hay thay đổi Execution Policy. Nếu máy không nhận `python` nhưng có Python Launcher, dùng `py -3.13 -m venv .venv` để tạo môi trường.

### 4. Mở demo

```powershell
.\.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

Giữ cửa sổ PowerShell mở và truy cập **[http://127.0.0.1:8501](http://127.0.0.1:8501)** bằng trình duyệt. Muốn dừng demo, nhấn **Ctrl+C** trong PowerShell.

**Những lần sau:** mở terminal trong thư mục dự án và chạy lại lệnh ở bước 4; không cần cài lại. Ảnh mẫu đã đi kèm, không cần chạy script tạo ảnh. Sau khi cài xong, demo có thể chạy không cần mạng.

### Lỗi thường gặp

| Hiện tượng | Cách xử lý |
| --- | --- |
| Không nhận `python` | Cài Python và bật Add Python to PATH, mở lại terminal; hoặc thử `py -3.13` |
| Không tìm thấy `app.py` hoặc `requirements.txt` | Chuyển vào thư mục dự án bằng `cd NMXLAChap3` |
| `No module named streamlit` | Chạy lại bước 3 và dùng đúng `.venv\Scripts\python` ở bước 4 |
| Cổng 8501 đang được sử dụng | Thêm `--server.port 8502` vào lệnh chạy, rồi mở `http://127.0.0.1:8502` |
| Trình duyệt không tự mở | Tự nhập địa chỉ demo; giữ terminal đang chạy |
| Không tải được thư viện | Kiểm tra mạng/proxy rồi chạy lại lệnh cài requirements |

### macOS / Linux

Sau khi cài Python 3.13 và tải dự án, chạy trong thư mục chứa `app.py`:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

Một số bản Linux cần cài thêm gói venv tương ứng với Python. Các lệnh macOS/Linux chưa được kiểm tra trực tiếp trong môi trường phát triển Windows này.

## Dùng demo lần đầu

1. Chọn ảnh mẫu hoặc tải ảnh ở thanh bên.
2. Chọn nội dung, kéo tham số và quan sát kết quả.
3. Bật **Hiện code Python** để xem các hàm đang dùng.
4. Trong **Tùy chỉnh không gian demo**, chọn số ảnh mỗi hàng và chiều cao ảnh.
5. Nhấn **Reset** để bắt đầu lại.

## Các màn hình

| Màn hình | Nội dung tương tác | Đối chiếu báo cáo |
| --- | --- | --- |
| Tổng quan | Ảnh / phổ Fourier, pipeline và công thức | Mục 2, Hình 1 |
| Convolution Theorem | Kernel 3–51, sigma 0.5–15, grid 2×3, hoạt cảnh 6 bước | Mục 2.2–3, Hình 2 |
| Gaussian Blur | Kernel 5/11/21/51, phổ kernel 2D/3D | Mục 3, Hình 2–3 |
| HPF | Cutoff 1–100, mask, kết quả có dấu, tăng cường biên, SNR thực | Mục 4.1, Hình 6–8 |
| LPF | Ideal / `fourier_gaussian`, tab khử nhiễu FFT, bật/tắt phổ | Mục 4.2 và 5.3 |
| BPF | Difference of Gaussians, hai sigma, kernel và phổ DoG | Mục 4.3, Hình 10 |
| Notch | Nhiễu sin, phát hiện đỉnh, click ứng viên / nhập tọa độ, cặp notch | Mục 4.4, Hình 11–12 |
| Image Restoration | Inverse có epsilon và noise; Wiener công thức / unsupervised | Mục 5.1–5.2, Hình 14,16 |
| So sánh Convolution | Direct vs FFT, 10–100 lần, boxplot, xuất JSON | Mục 3.1, Hình 4–5 |
| Tổng kết | Bảng bộ lọc, quy tắc lựa chọn | Mục 6–7, Bảng 1 |

Bám theo báo cáo 6 trang do người dùng cung cấp, không thêm CNN, deep learning
hay nhận dạng đối tượng. Demo phục hồi tập trung vào Gaussian như yêu cầu;
ví dụ motion blur được nhắc trong báo cáo không được thêm thành mục riêng.

## Quy ước tính toán để tránh hiểu sai

### Ảnh và phổ

- Upload PNG/JPEG/WebP, tối đa 15 MB / 25 megapixel. Đọc EXIF orientation,
  ghép alpha trên nền trắng, chuyển RGB sang grayscale bằng `rgb2gray`.
- Thu nhỏ cạnh dài tối đa 384 px, không phóng lớn; cạnh ngắn sau thu nhỏ ≥64 px.
  Ảnh 16-bit/float được từ chối có thông báo, không âm thầm chuyển sai thang.
- FFT tính trên float64, không chuẩn hóa min-max lại đầu ra để làm kết quả trông
  đẹp hơn. Dữ liệu phức giữ nguyên đến IFFT; không dùng `abs(IFFT)` thay ảnh có dấu.
- Phổ hiển thị `20*log10(1+abs(fftshift(F)))`; an toàn với giá trị 0.
  Các phổ ảnh trước/sau trong cùng thí nghiệm dùng chung giới hạn màu.
  Đáp ứng kernel/mask có thang riêng, ghi rõ trên panel.
- Kết quả HPF và DoG có dấu: đỏ dương, lam âm, trắng = 0; chỉ biểu diễn màu
  được co giãn đối xứng. Ảnh thông thường chỉ clip [0,1] khi hiển thị.
- Màu sáng của phổ là biên độ lớn, không phải độ sáng ở một vị trí trên ảnh.

### Tích chập và điều kiện biên

- Theorem/Gaussian/DoG: zero-pad tới `(M+K-1,N+L-1)`, nhân FFT, IFFT, crop
  `same`. Khớp tích chập **tuyến tính** với `scipy.signal.convolve` và `fftconvolve`.
- HPF/LPF/Notch và Restoration: mask/OTF trên lưới ảnh, tương ứng điều kiện
  **tuần hoàn** (tích chập vòng). Không trộn hai quy ước khi đối chiếu.
- PSF của Restoration được dịch đúng tâm về gốc trước FFT, kể cả ảnh kích thước lẻ.
- Gaussian hữu hạn có đuôi bị cắt. Nếu kernel quá nhỏ so với sigma, đáp ứng có
  thể có gợn và không còn là Gaussian liên tục lý tưởng; app ghi chú trường hợp này.
- Cutoff đo bằng khoảng cách **bin DFT** tới tâm; một bin tương ứng một chu kỳ
  trên chiều ảnh tương ứng. Với ảnh chữ nhật, bán kính bin không phải bán kính
  đẳng hướng theo chu kỳ/pixel. Nếu cutoff vượt giới hạn phổ ảnh nhỏ, mask có thể
  giữ/loại gần hết phổ — không phải lỗi.

### Notch

- Thêm sin có tần số nguyên để minh họa đỉnh đúng bin. Không clip ảnh nhiễu trước
  FFT vì clipping sinh thêm hài. Nhiễu âm/>1 chỉ bị clip trong hình xem.
- Ứng viên đỉnh lấy từ cực đại cục bộ của phổ ảnh nhiễu, bỏ vùng DC và lấy một
  nửa cặp đối xứng; **không dùng ảnh sạch để phát hiện**.
- Click dấu tròn ứng viên trong phổ hoặc nhập tọa độ tương đối so với tâm.
  Mask luôn loại cả `(u,v)` và `(-u,-v)`, có xử lý wrap tại Nyquist.
- Không gọi tất cả đỉnh là nhiễu. Chọn sai hoặc notch rộng có thể làm mất tín hiệu thật.

### Khôi phục

- Gây mờ và phục hồi dùng cùng kernel và cùng biên tuần hoàn, không lượng tử hóa
  ảnh mờ. Nhiễu Gaussian có seed 42 để tham số thay đổi trên cùng realization.
- Inverse: `F_hat = G/(H+epsilon)`; thêm ngưỡng số học rất nhỏ để tránh trường hợp
  PSF cắt hữu hạn có `H ≈ -epsilon`. Không hứa epsilon giải quyết hết vấn đề nhiễu.
- Wiener mặc định theo công thức (10): `H.conj()*G/(abs(H)**2+K)`.
  K mặc định dùng phương sai nhiễu / phương sai ảnh sạch trong thí nghiệm tổng hợp;
  ghi rõ đây không phải ước lượng mù. Có điều khiển K thủ công.
- Chế độ nâng cao dùng `skimage.restoration.unsupervised_wiener`, phù hợp ví dụ
  trong báo cáo, tối đa 50 vòng và seed 42, `clip=False`. Phải bấm chạy khi đổi đầu vào.
- Trước/sau có ba cặp lựa chọn: Gốc/Mờ, Mờ/Phục hồi, Gốc/Phục hồi.
- Sai khác hiển thị `abs(original-restored)` trên thang [0,1], kèm giá trị cực đại
  và tỷ lệ pixel vượt thang để không che giấu hiện tượng khuếch đại nhiễu.

### SNR và benchmark

- SNR dùng `10*log10(sum(f²)/sum((f-g)²))`, ảnh sạch/gốc làm tham chiếu,
  tính trên float chưa clip. Báo cáo không chỉ định công thức SNR, nên demo công bố
  quy ước riêng; không sao chép đường cong hay kết quả số của Hình 8.
- SNR tái tạo không phải điểm chất lượng cạnh. Với HPF lý tưởng, tăng cutoff
  loại thêm năng lượng ảnh gốc nên SNR theo quy ước này có thể giảm dù cạnh nổi hơn.
- `convolve(method='direct')` so với `fftconvolve`, cùng ảnh float64/kernel/biên zero.
  Ảnh benchmark thu nhỏ **giống nhau** về cạnh dài 64/96/128 px để 100 lần đo
  không khóa giao diện quá lâu. Kích thước này được hiển thị, không dùng kết quả
  để tuyên bố tốc độ trên ảnh độ phân giải đầy đủ.
- Warm-up một lần mỗi phương pháp, thứ tự chạy luân phiên, dùng `perf_counter_ns`.
  Không cache phép đo, không tính thời gian render/metrics vào thời gian thuật toán.
  Đổi ảnh/tham số sẽ ẩn kết quả cũ tới khi đo lại.

## Ảnh mẫu

Cameraman, Astronaut, Coffee, Chelsea và ảnh Patterns tổng hợp được lưu tại máy.
Không giả danh chúng là Lena/Mandrill/Parrot/Rhino. Đặt các ảnh mong muốn vào
`sample_images/` (PNG/JPEG/WebP); app tự nhận. Xem nguồn tại `sample_images/README.md`.

## Cấu trúc

```text
app.py                  # shell, sidebar, upload
views/                  # 10 mục giao diện
utils/fourier.py        # FFT, padding, OTF, phổ, SNR
utils/filters.py        # Gaussian, HPF, LPF, DoG, notch, phát hiện đỉnh
utils/restoration.py    # inverse, Wiener, unsupervised Wiener
utils/benchmark.py      # phép đo thực tế
utils/images.py         # đọc/chuẩn hóa ảnh
utils/ui.py             # panel, pipeline, slider, Plotly
assets/style.css
sample_images/
scripts/prepare_samples.py
tests/
```

## Kiểm tra

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py utils views scripts tests
pip check
```

Kiểm thử numerical bao gồm round-trip FFT, padding, vị trí PSF, mask đối xứng,
triệt sin bằng notch, khôi phục, xử lý upload và benchmark. AppTest kiểm tra
điều hướng, tham số, hai chế độ Wiener, Notch và Reset.

Tài liệu API: [NumPy FFT](https://numpy.org/doc/stable/reference/routines.fft.html),
[SciPy convolve](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve.html),
[Streamlit Plotly selection](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart).
