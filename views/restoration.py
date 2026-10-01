import hashlib
import numpy as np
import streamlit as st
from utils.filters import gaussian_kernel
from utils.restoration import degrade,inverse_filter,wiener_filter,automatic_wiener
from utils.ui import section,theory,panel_row,observation,before_after,metrics


@st.cache_data(show_spinner=False,max_entries=12)
def auto_restore(observed,kernel):
    return automatic_wiener(observed,kernel)


def render(image):
    section("Image Restoration","Biết mô hình gây mờ để ước lượng lại ảnh ban đầu.","08 · KHÔI PHỤC ẢNH")
    theory("Ảnh quan sát gồm ảnh gốc tích chập kernel và nhiễu. Demo dùng cùng PSF cho bước gây mờ và khôi phục, với điều kiện biên tuần hoàn; xử lý float64, không clip trung gian.",r"g=h*f+n\quad\Longleftrightarrow\quad G=HF+N")
    inverse,wiener=st.tabs(["A · Inverse Filter","B · Wiener Filter"])
    with inverse:
        with st.container(border=True):
            a,b,c=st.columns(3)
            sigma=a.slider("Blur Sigma · σ",.5,8.,2.,.5,key="inverse_sigma")
            size=b.select_slider("Kích thước kernel",options=[5,11,21,51],value=21,key="inverse_size")
            power=c.slider("Epsilon · ε = 10ⁿ",-6,-1,-3,key="inverse_epsilon")
            noise=st.toggle("Thêm nhiễu Gaussian",key="inverse_noise")
            level=st.slider("Độ lệch chuẩn nhiễu",.001,.05,.005,.001,key="inverse_noise_level") if noise else 0.
        epsilon=10.**power
        kernel=gaussian_kernel(size,sigma)
        observed,blurred,h=degrade(image,kernel,level)
        result=inverse_filter(observed,h,epsilon)
        difference=np.abs(image-result)
        st.latex(r"\hat F=\frac{G}{H+\varepsilon},\qquad \varepsilon="+f"{epsilon:g}")
        panel_row([("Ảnh gốc",image,"Tham chiếu sạch"),("Ảnh mờ"+(" + nhiễu" if noise else ""),observed,f"σ = {sigma:g} · noise σ = {level:g}"),
                   ("Inverse restored",result,"Chỉ clip [0,1] để hiển thị"),("Sai khác tuyệt đối",difference,"|f − f̂| · thang [0,1], không tự tăng tương phản")])
        metrics(image,observed,result)
        clipped=float(np.mean((result<0)|(result>1))*100)
        st.caption(f"{clipped:.2f}% pixel phục hồi nằm ngoài [0,1] trước hiển thị. Max |sai khác| = {difference.max():.4f}. Nhiễu có seed 42.")
        observation("Inverse Filter rất nhạy với nhiễu khi |H| nhỏ. Bật nhiễu rồi giảm epsilon để thấy nhiễu bị khuếch đại. Epsilon lớn ổn định hơn nhưng làm tăng sai lệch khôi phục.")
    with wiener:
        a,b,c=st.columns(3)
        sigma=a.slider("Mức mờ · σ",.5,8.,2.,.5,key="wiener_sigma")
        noise=b.slider("Mức nhiễu · độ lệch chuẩn",.001,.10,.015,.001,key="wiener_noise")
        size=c.select_slider("Kernel Gaussian",options=[5,11,21,51],value=21,key="wiener_size")
        kernel=gaussian_kernel(size,sigma)
        observed,blurred,h=degrade(image,kernel,noise)
        balance=max(noise**2/max(float(np.var(image)),1e-8),1e-6)
        method="Wiener theo công thức"
        if not st.session_state.presentation:
            with st.expander("Thiết lập khôi phục"):
                method=st.radio("Phương pháp Wiener",["Wiener theo công thức","Unsupervised Wiener · scikit-image"],key="wiener_method")
                manual=st.toggle("Tự chỉnh K",key="manual_k")
                if manual:
                    balance=10.**st.slider("log₁₀(K)",-6.,0.,-2.,.25,key="balance")
        st.latex(r"\hat F=\frac{H^*}{|H|^2+K}\,G")
        if method.startswith("Unsupervised"):
            signature=hashlib.sha256(observed.tobytes()+kernel.tobytes()).hexdigest()
            if st.button("Chạy Unsupervised Wiener",type="primary"):
                st.session_state.auto_wiener_signature=signature
            if st.session_state.get("auto_wiener_signature")!=signature:
                st.info("Bấm chạy để tự động ước lượng tham số và phục hồi ảnh bằng Unsupervised Wiener.")
                return
            with st.spinner("Đang ước lượng Wiener · tối đa 50 vòng lặp..."):
                result=auto_restore(observed,kernel)
            st.caption("Unsupervised Wiener ước lượng tham số từ ảnh quan sát; seed 42, tối đa 50 vòng. Không dùng K của công thức đơn giản bên trên.")
        else:
            result=wiener_filter(observed,h,balance)
            st.caption(f"K = {balance:.5g}. Mặc định ước lượng bằng phương sai nhiễu / phương sai ảnh sạch trong thí nghiệm tổng hợp, không phải ước lượng mù trên ảnh thực.")
        panel_row([("Ảnh gốc",image,"Tham chiếu sạch"),("Ảnh mờ + nhiễu",observed,f"σ mờ {sigma:g} · σ nhiễu {noise:g}"),("Wiener restored",result,"Khử mờ có điều hòa")])
        pair=st.segmented_control("So sánh trực tiếp",["Mờ / Phục hồi","Gốc / Phục hồi","Gốc / Mờ"],default="Mờ / Phục hồi",key="restore_pair")
        before,after,left,right={"Mờ / Phục hồi":(observed,result,"MỜ + NHIỄU","WIENER RESTORED"),
            "Gốc / Phục hồi":(image,result,"ẢNH GỐC","WIENER RESTORED"),"Gốc / Mờ":(image,observed,"ẢNH GỐC","MỜ + NHIỄU")}[pair]
        before_after(before,after,left,right,height=410 if st.session_state.presentation else 350)
        metrics(image,observed,result)
        observation("Wiener cân bằng khử mờ và hạn chế khuếch đại nhiễu. K quá nhỏ dễ tăng nhiễu; K quá lớn làm ảnh mượt và mất chi tiết. Khả năng phục hồi phụ thuộc PSF, nhiễu và tham số, không đảm bảo phục hồi hoàn hảo.")
