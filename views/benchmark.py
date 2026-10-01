import hashlib
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import streamlit as st
from utils.filters import gaussian_kernel
from utils.benchmark import benchmark
from utils.ui import section,theory,panel_row,observation


def render(image):
    section("So sánh Convolution","Cùng ảnh, cùng kernel, cùng điều kiện biên. Đo ngay trên máy đang chạy.","09 · BENCHMARK")
    theory("scipy.signal.convolve(method='direct') buộc dùng tích chập trực tiếp. Nếu để method='auto', SciPy có thể tự chọn FFT, khiến so sánh không còn rõ ràng. Cả hai dùng float64, mode='same', biên zero.")
    with st.container(border=True):
        a,b,c,d=st.columns(4)
        side=a.select_slider("Cạnh dài ảnh benchmark",options=[64,96,128],value=96,key="bench_side")
        size=b.slider("Kernel (lẻ)",3,31,11,2,key="bench_size")
        sigma=c.slider("Sigma Gaussian",.5,10.,3.,.5,key="bench_sigma")
        repeats=d.slider("Số lần đo mỗi phương pháp",10,100,10,10,key="bench_repeats")
    resized=Image.fromarray(image.astype(np.float32),mode="F")
    resized.thumbnail((side,side),Image.Resampling.BILINEAR)
    small=np.asarray(resized,dtype=np.float64)
    kernel=gaussian_kernel(size,sigma)
    signature=hashlib.sha256(small.tobytes()+kernel.tobytes()+str(repeats).encode()).hexdigest()
    st.caption(f"Ảnh thử: {small.shape[1]} × {small.shape[0]} px, cùng phiên bản thu nhỏ cho cả hai phép tính. Làm nóng mỗi phương pháp một lần, đổi thứ tự chạy luân phiên; không dùng cache cho phép đo.")
    if st.button("▶ Chạy đo thực tế · Run Benchmark",type="primary"):
        progress=st.progress(0.,text="Đang đo thời gian thực thi...")
        results=benchmark(small,kernel,repeats,progress=lambda value:progress.progress(value,text="Đang đo thời gian thực thi..."))
        st.session_state.benchmark_result=(signature,results)
        progress.empty()
    saved=st.session_state.get("benchmark_result")
    if not saved or saved[0]!=signature:
        st.info("Bấm Run Benchmark để tạo kết quả. Khi đổi ảnh hoặc tham số, cần chạy phép đo mới.")
        panel_row([("Ảnh benchmark",small,"Cùng đầu vào cho hai phương pháp"),("Gaussian kernel",kernel,f"{size}×{size} · σ={sigma:g}","kernel")])
        return
    outputs,times,error=saved[1]
    names=list(times)
    panel_row([("Ảnh gốc",small,"Ảnh đã thu nhỏ"),
        ("convolve() · direct",outputs[names[0]],f"Trung bình {np.mean(times[names[0]]):.3f} ms"),
        ("fftconvolve()",outputs[names[1]],f"Trung bình {np.mean(times[names[1]]):.3f} ms")])
    winner=min(times,key=lambda name:np.mean(times[name]))
    st.success(f"Nhanh hơn trong phép đo này: {winner} · Sai khác đầu ra tối đa: {error:.2e}")
    fig=go.Figure()
    for name,color in zip(names,["#8aa5af","#267969"]):
        fig.add_trace(go.Box(y=times[name],name=name,boxpoints="all",jitter=.2,marker_color=color))
    fig.update_layout(height=310,yaxis_title="Thời gian (ms)",showlegend=False,margin=dict(l=10,r=10,t=10,b=20),paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,width="stretch",key="benchmark_box")
    rows=[{"Phương pháp":name,"Trung bình (ms)":float(np.mean(vals)),"Nhỏ nhất (ms)":min(vals),"Lớn nhất (ms)":max(vals),"Số lần":len(vals)} for name,vals in times.items()]
    st.dataframe(rows,hide_index=True,width="stretch")
    import json
    st.download_button("↓ Tải dữ liệu đo",json.dumps({"shape":list(small.shape),"kernel":size,"sigma":sigma,"times_ms":times,"max_abs_error":error},indent=2),"benchmark.json","application/json")
    observation("FFT không luôn nhanh hơn trong mọi cấu hình. Thời gian phụ thuộc kích thước ảnh, kernel, phần cứng và tải máy. Kết quả được đo trực tiếp trên máy.")
