# Thư viện ảnh offline

Ảnh mẫu thực tế được kèm theo dự án, không tải khi mở app:

- `cameraman.png`: scikit-image `data.camera`, public domain.
- `astronaut.png`: scikit-image `data.astronaut`, NASA / Eileen Collins, public domain.
- `coffee.png`: scikit-image `data.coffee`, Rachel Michetti, CC0.
- `chelsea.png`: scikit-image `data.chelsea`, Stefan van der Walt, CC0.
- `patterns.png`: ảnh hình học và sóng sin tạo bằng script của dự án.

Nguồn: https://scikit-image.org/docs/stable/api/skimage.data.html

Không gán tên Lena/Mandrill/Parrot/Rhino cho ảnh thay thế. Nếu có các ảnh này,
đặt `lena.png`, `mandrill.png`, `parrot.png`, `rhino.png` vào thư mục này; app
tự nhận và hiển thị đúng tên. Có thể thêm ảnh PNG/JPEG/WebP bất kỳ hoặc upload.
Các file bổ sung cần có quyền sử dụng phù hợp.

Tái tạo bộ ảnh hiện có: `python scripts/prepare_samples.py`.
