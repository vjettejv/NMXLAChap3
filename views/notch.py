import hashlib
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.filters import periodic_noise,detect_peaks,notch_mask
from utils.fourier import fft_image,spectrum,frequency_grid,apply_mask
from utils.ui import section,theory,panel_row,panel,observation,metrics,before_after,spectrum_note


def render(image):
    section("Notch Filter","Tìm nhiễu tuần hoàn trên phổ. Loại đúng tần số gây nhiễu.","07 · NHIỄU TUẦN HOÀN")
    theory("Một sóng sin trong ảnh tạo ra cặp đỉnh đối xứng trong phổ. Notch loại đồng thời cả hai đỉnh để giữ kết quả IFFT là ảnh thực.",r"g(x,y)=f(x,y)+A\sin\left[2\pi\left(\frac{k_x x}{N}+\frac{k_y y}{M}\right)\right]")
    with st.container(border=True):
        a,b,c=st.columns(3)
        fx=a.slider("Tần số ngang · kₓ",1,min(100,image.shape[1]//2-1),min(32,image.shape[1]//4),key="notch_fx")
        fy=b.slider("Tần số dọc · kᵧ",0,min(100,image.shape[0]//2-1),min(12,image.shape[0]//4),key="notch_fy")
        strength=c.slider("Biên độ nhiễu sin · A",.02,.5,.2,.02,key="notch_strength")
        if st.button("① Thêm nhiễu tuần hoàn · Add Periodic Noise",type="primary"):
            st.session_state.notch_added=True
        st.caption("Tần số tính bằng số chu kỳ trên chiều ảnh. Nhiễu không bị clip trước FFT; ảnh hiển thị được giới hạn về [0,1].")
    if not st.session_state.get("notch_added",False):
        panel_row([("Ảnh gốc",image,"Chưa thêm nhiễu"),("Phổ ảnh gốc",spectrum(fft_image(image)),"Nhấn nút để bắt đầu","spectrum")])
        observation("Thêm nhiễu để thấy sọc xuất hiện, tìm cặp đỉnh trên phổ rồi áp dụng notch. Tham số cập nhật trực tiếp sau lần thêm nhiễu đầu tiên.")
        return
    noisy=periodic_noise(image,fx,fy,strength)
    original_spec=spectrum(fft_image(image)); noisy_spec=spectrum(fft_image(noisy))
    maximum=float(max(original_spec.max(),noisy_spec.max()))
    panel_row([("Ảnh gốc",image,"Tham chiếu sạch"),("Phổ ảnh gốc",original_spec,"Chưa có nhiễu sin","spectrum",maximum)])
    candidates=detect_peaks(noisy)
    if not candidates:
        st.warning("Không tìm được đỉnh phù hợp. Hãy dùng tọa độ notch thủ công.")
        candidates=[(fx,fy,0.)]
    selection=st.segmented_control("Chọn vị trí notch",["Đỉnh phát hiện trên phổ","Nhập tọa độ"],default="Đỉnh phát hiện trên phổ",key="notch_selection")
    if selection=="Nhập tọa độ":
        a,b=st.columns(2)
        px=a.number_input("Tọa độ u so với tâm",-(image.shape[1]//2),image.shape[1]//2-1,value=fx,key="manual_u")
        py=b.number_input("Tọa độ v so với tâm",-(image.shape[0]//2),image.shape[0]//2-1,value=fy,key="manual_v")
    else:
        px,py,_=candidates[0]
    col1,col2=st.columns(2)
    with col1:
        panel("Ảnh nhiễu tuần hoàn",noisy,f"Sóng sin ({fx}, {fy}) · A = {strength:.2f}")
    with col2:
        st.markdown("**Phổ nhiễu · chọn một dấu tròn để đặt notch**")
        x,y=frequency_grid(image.shape)
        stride=max(1,max(image.shape)//256)
        fig=go.Figure(go.Heatmap(x=x[0,::stride],y=y[::stride,0],z=noisy_spec[::stride,::stride],
            colorscale="Magma",zmin=0,zmax=maximum,showscale=False,hovertemplate="u=%{x:.0f}, v=%{y:.0f}<br>Phổ log=%{z:.2f}<extra></extra>"))
        cx=[sign*p[0] for p in candidates for sign in (1,-1)]
        cy=[sign*p[1] for p in candidates for sign in (1,-1)]
        fig.add_trace(go.Scatter(x=cx,y=cy,mode="markers",marker=dict(size=13,color="#77ffd0",symbol="circle-open",line=dict(width=2)),
            customdata=list(zip(cx,cy)),name="Đỉnh ứng viên",hovertemplate="Chọn notch (%{x}, %{y})<extra></extra>"))
        fig.update_layout(height=300,margin=dict(l=20,r=10,t=10,b=20),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#102631",
            xaxis=dict(title="u · bin DFT",constrain="domain"),yaxis=dict(title="v · bin DFT",autorange="reversed",scaleanchor="x"),
            clickmode="event+select",dragmode="select",showlegend=False)
        digest=hashlib.sha256(image.tobytes()).hexdigest()[:10]
        event=st.plotly_chart(fig,width="stretch",key=f"peak_{digest}_{fx}_{fy}_{strength}",on_select="rerun",selection_mode="points",config={"displayModeBar":False})
        points=event.selection.points
        if selection=="Đỉnh phát hiện trên phổ" and points:
            point=points[-1]
            if point.get("curve_number",point.get("curveNumber"))==1 or "customdata" in point:
                px,py=int(round(point["x"])),int(round(point["y"]))
    st.caption(f"Notch đang chọn: ({px}, {py}) và ({-px}, {-py}). Vòng tròn là đỉnh ứng viên phát hiện từ phổ nhiễu, không phải kết luận mọi đỉnh đều là nhiễu.")
    spectrum_note(maximum)
    radius=st.slider("Bán kính notch (bin)",1,12,2,key="notch_radius")
    if px==0 and py==0:
        st.warning("Bạn đang loại thành phần DC: độ sáng trung bình của ảnh sẽ bị mất.")
    if st.button("② Áp dụng Notch Filter",type="primary"):
        st.session_state.notch_applied=True
    if st.session_state.get("notch_applied",False):
        mask=notch_mask(image.shape,px,py,radius)
        result,f,g=apply_mask(noisy,mask)
        panel_row([("Notch mask",mask,"Loại cặp vùng đối xứng","mask"),
                   ("Phổ sau lọc",spectrum(g),"Cùng thang màu với phổ đầu vào","spectrum",maximum),
                   ("Ảnh phục hồi",result,"IFFT của phổ đã lọc")])
        before_after(noisy,result,left="ẢNH CÓ NHIỄU SỌC",right="SAU NOTCH FILTER")
        metrics(image,noisy,result)
    observation("Nhiễu tuần hoàn tập trung tại một số tần số xác định. Chọn đúng cặp đỉnh giúp giảm sọc; notch quá rộng hoặc sai vị trí sẽ loại bỏ cả thông tin thật của ảnh. Kết quả không nhất thiết giống hoàn toàn ảnh gốc.")
