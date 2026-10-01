import numpy as np
import streamlit as st
from scipy.signal import fftconvolve
from utils.filters import gaussian_kernel
from utils.fourier import linear_fft_convolve,spectrum
from utils.ui import section,theory,panel_row,pipeline,observation,spectrum_note,surface


@st.cache_data(show_spinner=False,max_entries=16)
def compute(image,size,sigma):
    kernel=gaussian_kernel(size,sigma)
    result,f,h,g=linear_fft_convolve(image,kernel)
    error=float(np.max(np.abs(result-fftconvolve(image,kernel,mode="same"))))
    return kernel,result,f,h,g,error


def render(image,gaussian=False):
    prefix="gaussian" if gaussian else "theorem"
    section("Gaussian Blur" if gaussian else "Convolution Theorem",
            "Làm mờ trong miền không gian, suy giảm cao tần trong miền Fourier." if gaussian else "Tích chập ở một miền. Phép nhân ở miền còn lại.","03 · GAUSSIAN" if gaussian else "02 · ĐỊNH LÝ TÍCH CHẬP")
    theory("Ảnh và kernel được zero-pad tới M+K−1 × N+K−1. Nhân phổ rồi IFFT cho tích chập tuyến tính; cắt tâm về kích thước ảnh, giống mode='same'.",
           r"F=\operatorname{FFT}(f),\quad H=\operatorname{FFT}(h),\quad G=F\cdot H,\quad g=\operatorname{IFFT}(G)")
    with st.container(border=True):
        a,b,c=st.columns([1,1.3,1])
        if gaussian:
            size=a.select_slider("Kích thước kernel",options=[5,11,21,51],value=21,key=prefix+"_size")
        else:
            size=a.slider("Kích thước kernel (lẻ)",3,51,11,2,key=prefix+"_size")
        sigma=b.slider("Độ rộng Gaussian · σ",.5,15.,3.,.5,key=prefix+"_sigma")
        c.caption("σ tính bằng pixel trong miền không gian. Kernel được chuẩn hóa có tổng bằng 1.")
    kernel,result,f,h,g,error=compute(image,size,sigma)
    if not gaussian:
        animate=st.button("▶ Minh họa từng bước · Animate Process",type="primary")
        pipeline(animate=animate,image=image,result=result)
    original_spec=spectrum(f); maximum=float(original_spec.max())
    panel_row([("Ảnh gốc · f(x,y)",image,"Miền không gian"),
               ("Gaussian kernel · h(x,y)",kernel,f"{size} × {size} · σ = {sigma:g} · tổng = 1","kernel"),
               ("Ảnh sau tích chập · g(x,y)",result,"IFFT → cắt vùng same")])
    panel_row([("Phổ ảnh · F(u,v)",original_spec,"FFT trên ảnh zero-pad","spectrum",maximum),
               ("Đáp ứng kernel · |H(u,v)|",np.abs(np.fft.fftshift(h)),"Tâm = DC, biên độ cực đại 1","mask"),
               ("Phổ đầu ra · G(u,v)",spectrum(g),"Phổ của kết quả full trước khi crop","spectrum",maximum)])
    spectrum_note(maximum)
    st.caption(f"Sai khác lớn nhất so với scipy.signal.fftconvolve: {error:.2e}. Điều kiện biên: zero-padding, không phải tích chập vòng.")
    if gaussian:
        mode=st.segmented_control("Quan sát đáp ứng Gaussian",["2D Spectrum","3D Spectrum"],default="3D Spectrum",key="gaussian_view")
        if mode=="3D Spectrum":
            surface(np.abs(np.fft.fftshift(h)),"gaussian_3d")
        else:
            from utils.ui import panel
            panel("Phổ Gaussian 2D",np.abs(np.fft.fftshift(h)),"Biên độ tuyến tính |H|","mask")
    if size < 6*sigma+1:
        st.caption("Kernel nhỏ so với σ nên đuôi Gaussian bị cắt đáng kể; đáp ứng rời rạc có thể xuất hiện gợn. Tăng kernel để gần Gaussian lý tưởng hơn.")
    observation("Khi σ tăng, ảnh thường mờ hơn và đáp ứng giữ tần số thấp hẹp lại. Gaussian là LPF: làm suy giảm chi tiết biến thiên nhanh. Với kernel hữu hạn, mức mờ còn bị giới hạn bởi kích thước kernel.")
