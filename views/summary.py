import streamlit as st
from utils.ui import section,observation
from views.overview import go


def render(image):
    section("Chọn đúng miền tần số","Bắt đầu từ vấn đề của ảnh, rồi chọn vùng phổ cần giữ hoặc loại.","10 · TỔNG KẾT")
    rows=[
        {"Bộ lọc":"HPF","Tần số":"Giữ cao tần","Tác động":"Nhấn biên / chi tiết","Ứng dụng":"Tăng cường biên","Đánh đổi":"Có thể làm nhiễu nổi bật"},
        {"Bộ lọc":"LPF","Tần số":"Giữ thấp tần","Tác động":"Làm mịn","Ứng dụng":"Làm mờ / giảm nhiễu","Đánh đổi":"Mất chi tiết, ringing với mask lý tưởng"},
        {"Bộ lọc":"BPF / DoG","Tần số":"Giữ dải trung gian","Tác động":"Nhấn cấu trúc theo thang","Ứng dụng":"Làm nổi texture / cạnh","Đánh đổi":"Phụ thuộc dải chọn"},
        {"Bộ lọc":"Notch","Tần số":"Loại một số vùng hẹp","Tác động":"Giảm nhiễu tuần hoàn","Ứng dụng":"Loại sọc sin","Đánh đổi":"Có thể mất tín hiệu thật"},
        {"Bộ lọc":"Inverse","Tần số":"Bù đáp ứng gây mờ H","Tác động":"Khử mờ","Ứng dụng":"Biết kernel suy giảm","Đánh đổi":"Rất nhạy với nhiễu"},
        {"Bộ lọc":"Wiener","Tần số":"Bù H có điều hòa","Tác động":"Khử mờ và hạn chế nhiễu","Ứng dụng":"Ảnh vừa mờ vừa nhiễu","Đánh đổi":"Cần mô hình / ước lượng"},
    ]
    st.dataframe(rows,hide_index=True,width="stretch")
    st.markdown("### Ảnh của bạn cần gì?")
    choices=[("Làm mịn?","LPF","LPF – Low-pass Filter"),("Nhấn cạnh, chi tiết?","HPF","HPF – High-pass Filter"),
             ("Chọn một dải tần?","BPF / DoG","BPF – Band-pass Filter"),("Có nhiễu tuần hoàn?","Notch","Notch Filter"),
             ("Biết kernel, ít nhiễu?","Inverse","Image Restoration"),("Ảnh vừa mờ vừa nhiễu?","Wiener","Image Restoration")]
    for start in (0,3):
        for col,(problem,method,target) in zip(st.columns(3),choices[start:start+3]):
            with col:
                st.markdown(f'<div class="feature"><span>VẤN ĐỀ → PHƯƠNG PHÁP</span><b>{problem}</b><p>→ {method}</p></div>',unsafe_allow_html=True)
                st.button(f"Khám phá {method} →",key="summary_"+method,width="stretch",on_click=go,args=(target,))
    observation("Xử lý miền tần số giúp phân tích và điều chỉnh trực tiếp các thành phần tần số của ảnh. Hiệu quả phụ thuộc mô hình suy giảm, đặc tính nhiễu và tham số; không có bộ lọc tốt nhất cho mọi trường hợp.")
    with st.expander("Kịch bản trình bày 7–10 phút",expanded=st.session_state.presentation):
        st.markdown("""1. **Tổng quan (45 giây):** đối chiếu ảnh với phổ; giải thích tâm phổ.
2. **Convolution Theorem (1 phút):** chạy hoạt cảnh DFT → nhân phổ → IDFT.
3. **Gaussian (1 phút):** tăng sigma, xoay phổ 3D để thấy đặc tính LPF.
4. **HPF / LPF / BPF (2 phút):** đổi cutoff và sigma; quan sát phần chi tiết bị mất.
5. **Notch (1–2 phút):** thêm sọc, chọn cặp đỉnh, áp dụng notch, kéo trước/sau.
6. **Restoration (1–2 phút):** bật nhiễu ở Inverse rồi so với Wiener.
7. **Benchmark và tổng kết (1 phút):** chạy 10 lần với kernel 11×11, đọc số thực tế.""")
