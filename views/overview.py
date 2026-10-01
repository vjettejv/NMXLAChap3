import streamlit as st
from utils.fourier import fft_image,spectrum
from utils.ui import panel,pipeline,observation


def render(image):
    left,right=st.columns([1.05,1],gap="large",vertical_alignment="center")
    with left:
        st.markdown('<span class="pill">KHÁM PHÁ XỬ LÝ ẢNH</span>'
            '<div class="hero-title">Một bức ảnh.<br>Hai miền biểu diễn.<br><em>Nhiều cách khám phá.</em></div>'
            '<p class="hero-copy">Từ pixel đến phổ Fourier. Khám phá cách tích chập, lọc tần số và khôi phục ảnh qua từng thao tác trực tiếp.</p>',unsafe_allow_html=True)
        st.button("Bắt đầu với định lý tích chập →",type="primary",on_click=go,args=("Convolution Theorem",))
    with right:
        a,b=st.columns(2,gap="small")
        with a: panel("Miền không gian",image,"f(x,y) · Ảnh mức xám")
        with b: panel("Miền tần số",spectrum(fft_image(image)),"F(u,v) · Phổ log đã dịch tâm","spectrum")
    st.markdown('<div class="section-label">TỪ ẢNH ĐẦU VÀO ĐẾN ẢNH KẾT QUẢ</div>',unsafe_allow_html=True)
    pipeline()
    a,b=st.columns(2)
    a.latex(r"g(x,y)=f(x,y)*h(x,y)")
    b.latex(r"G(u,v)=F(u,v)H(u,v)")
    observation("Định lý tích chập cho phép chuyển phép tích chập trong miền không gian thành phép nhân trong miền tần số. Tâm phổ chứa tần số thấp; càng xa tâm, biến thiên càng nhanh. Độ sáng của phổ biểu diễn biên độ, không phải độ sáng tại một vị trí trong ảnh.")
    cards=[("01 / BIẾN ĐỔI","Tích chập & Gaussian","Quan sát ảnh, kernel và phổ tương ứng.","Gaussian Blur"),
           ("02 / CHỌN TẦN SỐ","HPF, LPF & Notch","Giữ vùng phổ hữu ích, loại thành phần gây nhiễu.","Notch Filter"),
           ("03 / KHÔI PHỤC","Inverse & Wiener","Khám phá sự đánh đổi giữa khử mờ và nhiễu.","Image Restoration")]
    for col,(number,title,body,target) in zip(st.columns(3),cards):
        with col:
            st.markdown(f'<div class="feature"><span>{number}</span><b>{title}</b><p>{body}</p></div>',unsafe_allow_html=True)
            st.button("Khám phá →",key=target,width="stretch",on_click=go,args=(target,))


def go(page):
    st.session_state.page=page
