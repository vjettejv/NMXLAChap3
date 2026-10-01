import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.filters import ideal_mask,gaussian_lpf,dog_kernel
from utils.fourier import apply_mask,fft_image,spectrum,linear_fft_convolve,snr
from utils.ui import section,theory,panel_row,observation,spectrum_note,panel,metrics,before_after


@st.cache_data(show_spinner=False,max_entries=8)
def cutoff_curve(image):
    xs=np.arange(1,101,5)
    ys=[snr(image,apply_mask(image,ideal_mask(image.shape,c,True))[0]) for c in xs]
    return xs,ys


def filter_panels(image,result,f,g,mask,high=False):
    maximum=float(spectrum(f).max())
    panel_row([("Ảnh đầu vào",image,"Mức xám [0,1]"),
        ("Phổ đầu vào",spectrum(f),"Trước lọc","spectrum",maximum),
        ("Mask · H(u,v)",mask,"Tối = loại bỏ · Sáng = giữ","mask")])
    panel_row([("Phổ sau lọc",spectrum(g),"G = F × H","spectrum",maximum),
        ("Kết quả lọc",result,"Có dấu: đỏ dương, lam âm; nền trắng = 0" if high else "Ảnh sau IFFT", "signed" if high else "image")])
    spectrum_note(maximum)


def render_hpf(image):
    section("HPF · Bộ lọc thông cao","Loại vùng thấp tần ở tâm phổ để quan sát cạnh và chi tiết.","04 · HIGH-PASS FILTER")
    theory("HPF lý tưởng loại các tần số có khoảng cách tới tâm ≤ cutoff. Các cạnh, chi tiết nhỏ và cả nhiễu đều có thể đóng góp vào cao tần.",r"H_{HP}(u,v)=\begin{cases}0&D(u,v)\le D_0\\1&D(u,v)>D_0\end{cases}")
    a,b=st.columns([2,1])
    cutoff=a.slider("Tần số cắt · D₀ (bin DFT)",1,100,20,key="hpf_cutoff")
    enhance=b.toggle("Tăng cường biên trên ảnh gốc",key="hpf_enhance")
    mask=ideal_mask(image.shape,cutoff,True)
    result,f,g=apply_mask(image,mask)
    filter_panels(image,result,f,g,mask,True)
    if enhance:
        amount=st.slider("Hệ số tăng cường α",.1,3.,1.,.1,key="edge_amount")
        before_after(image,image+amount*result,right="ẢNH GỐC + α·HPF")
        st.caption("Tăng cường biên dùng f + α·HPF(f), chỉ clip về [0,1] khi hiển thị.")
    with st.expander("Tần số cắt và SNR · số liệu thực",expanded=not st.session_state.presentation):
        xs,ys=cutoff_curve(image)
        fig=go.Figure(go.Scatter(x=xs,y=ys,mode="lines+markers",line=dict(color="#267969"),name="SNR"))
        fig.add_vline(x=cutoff,line_dash="dot",line_color="#c97e39")
        fig.update_layout(height=260,margin=dict(l=10,r=10,t=15,b=20),xaxis_title="Cutoff D₀ (bin DFT)",yaxis_title="SNR (dB)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white")
        st.plotly_chart(fig,width="stretch",key="snr_curve")
        st.latex(r"\mathrm{SNR}=10\log_{10}\frac{\sum f^2}{\sum(f-g)^2}")
        st.caption("Ảnh gốc làm tham chiếu, g là HPF thuần chưa tăng cường. Đây là độ gần ảnh gốc, không phải điểm chất lượng đường biên. Báo cáo không quy định công thức SNR; demo công bố quy ước này.")
    observation("Cutoff tăng → loại nhiều thấp tần hơn → mất thêm thông tin nền và mức xám tổng thể. Cạnh có thể nổi bật tương đối, nhưng không có nghĩa giữ được nhiều cạnh hơn. Ngưỡng cắt gắt có thể tạo ringing quanh biên.")


def render_lpf(image):
    section("LPF · Bộ lọc thông thấp","Giữ thành phần biến thiên chậm, làm dịu chi tiết cao tần.","05 · LOW-PASS FILTER")
    theory("LPF giữ tần số thấp và suy giảm cao tần. Gaussian LPF sử dụng trực tiếp scipy.ndimage.fourier_gaussian trên FFT chưa shift.",r"H_{LP}(u,v)=\begin{cases}1&D(u,v)\le D_0\\0&D(u,v)>D_0\end{cases}")
    smooth,denoise=st.tabs(["Làm mịn · LPF","Khử nhiễu bằng FFT"])
    with smooth:
        mode=st.segmented_control("Dạng bộ lọc",["Ideal LPF","Gaussian LPF"],default="Ideal LPF",key="lpf_mode")
        if mode=="Gaussian LPF":
            sigma=st.slider("Sigma không gian · σ",1.,15.,3.,.5,key="lpf_sigma")
            result,f,g,mask=gaussian_lpf(image,sigma)
        else:
            cutoff=st.slider("Tần số cắt · D₀ (bin DFT)",1,100,30,key="lpf_cutoff")
            mask=ideal_mask(image.shape,cutoff)
            result,f,g=apply_mask(image,mask)
        filter_panels(image,result,f,g,mask)
        observation("Với Ideal LPF, cutoff thấp làm ảnh mờ hơn; tăng cutoff cho thêm chi tiết đi qua. Với Gaussian LPF, σ không gian lớn làm ảnh mờ hơn. Làm mịn có thể giảm nhiễu cao tần nhưng cũng làm mất chi tiết thật.")
    with denoise:
        a,b=st.columns(2)
        noise_sigma=a.slider("Độ lệch chuẩn nhiễu Gaussian",.01,.2,.06,.01,key="fft_noise")
        cutoff=b.slider("Ngưỡng tần số giữ lại",1,100,45,key="fft_cutoff")
        noisy=image+np.random.default_rng(42).normal(0,noise_sigma,image.shape)
        mask=ideal_mask(image.shape,cutoff)
        result,f,g=apply_mask(noisy,mask)
        st.caption("Ảnh nhiễu → FFT → Phổ → LPF mask → Phổ sau lọc → IFFT → Ảnh giảm nhiễu")
        panel_row([("Ảnh nhiễu",noisy,"Nhiễu tổng hợp · seed 42"),("LPF mask",mask,"Giữ vùng trung tâm","mask"),("Ảnh sau lọc",result,"Có thể mất chi tiết")])
        a,b=st.columns(2)
        show_input=a.toggle("Hiện phổ ảnh nhiễu",value=True,key="fft_show_input")
        show_output=b.toggle("Hiện phổ đã lọc",value=True,key="fft_show_output")
        maximum=float(spectrum(f).max())
        with a:
            if show_input: panel("Phổ ảnh nhiễu",spectrum(f),"Thang log chung","spectrum",maximum)
        with b:
            if show_output: panel("Phổ đã lọc",spectrum(g),"Thang log chung","spectrum",maximum)
        metrics(image,noisy,result)
        observation("Lọc FFT chỉ hiệu quả nếu vùng tần số bị loại chứa nhiều nhiễu hơn thông tin cần giữ. Gaussian noise phân bố rộng, nên LPF không thể tách nhiễu hoàn hảo khỏi ảnh.")


def render_bpf(image):
    section("BPF · Difference of Gaussians","Lấy hiệu hai mức làm mờ để nhấn mạnh một dải cấu trúc.","06 · BAND-PASS FILTER")
    theory("DoG lấy Gaussian hẹp trừ Gaussian rộng, tổng kernel gần 0 nên loại thành phần DC. Dải thông mềm, không phải vành đai cắt tuyệt đối.",r"h_{DoG}=G(\sigma_1)-G(\sigma_2),\qquad 0<\sigma_1<\sigma_2")
    a,b=st.columns(2)
    sigma1=a.slider("Sigma 1 · Gaussian hẹp",.5,10.,1.5,.5,key="dog_s1")
    sigma2=b.slider("Sigma 2 · Gaussian rộng",1.,15.,4.,.5,key="dog_s2")
    if sigma1>=sigma2:
        st.warning("Để tạo DoG đúng hướng, hãy chọn Sigma 1 nhỏ hơn Sigma 2.")
        return
    size=51
    from utils.filters import gaussian_kernel
    k1,k2=gaussian_kernel(size,sigma1),gaussian_kernel(size,sigma2)
    a1,*_=linear_fft_convolve(image,k1)
    a2,*_=linear_fft_convolve(image,k2)
    kernel=dog_kernel(size,sigma1,sigma2)
    result,f,h,g=linear_fft_convolve(image,kernel)
    panel_row([("Ảnh gốc",image,"Miền không gian"),("Gaussian 1",a1,f"σ₁ = {sigma1:g}"),("Gaussian 2",a2,f"σ₂ = {sigma2:g}")])
    panel_row([("DoG kernel",kernel,"Kernel 51×51 · đỏ dương, lam âm","signed"),
               ("DoG Spectrum",np.abs(np.fft.fftshift(h)),"DC bị triệt; hiển thị biên độ tương đối","kernel"),
               ("Band-pass output",result,"Đỏ dương, lam âm · nền trắng = 0","signed")])
    observation("Những cấu trúc khác nhau giữa hai mức làm mờ trở nên nổi bật. Thay đổi hai sigma để chọn thang chi tiết; sigma quá gần nhau cho đáp ứng yếu. Màu của kết quả biểu diễn dấu và biên độ, không phải màu gốc.")
