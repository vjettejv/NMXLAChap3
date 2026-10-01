from pathlib import Path
import hashlib
import streamlit as st
from utils.images import available_samples,DISPLAY_NAMES,read_image
from views import overview,convolution,frequency,notch,restoration,benchmark,summary

st.set_page_config(page_title="Fourier Lab · Nhóm 1",page_icon="◈",layout="wide",initial_sidebar_state="expanded")
ROOT=Path(__file__).parent
st.markdown(f"<style>{(ROOT/'assets/style.css').read_text(encoding='utf-8')}</style>",unsafe_allow_html=True)
PAGES=["Tổng quan","Convolution Theorem","Gaussian Blur","HPF – High-pass Filter","LPF – Low-pass Filter",
       "BPF – Band-pass Filter","Notch Filter","Image Restoration","So sánh Convolution","Tổng kết"]
for key,value in {"page":"Tổng quan","presentation":False,"upload_epoch":0,"source":"Ảnh mẫu"}.items():
    st.session_state.setdefault(key,value)


def reset():
    epoch=st.session_state.upload_epoch+1
    for key in list(st.session_state):
        del st.session_state[key]
    st.session_state.update(page="Tổng quan",presentation=False,upload_epoch=epoch,source="Ảnh mẫu")


def load_sample():
    st.session_state.source="Ảnh mẫu"


samples=available_samples()
with st.sidebar:
    st.markdown('<div class="side-logo"><div class="logo-symbol">∿</div><div><strong>FOURIER LAB</strong><small>IMAGE PROCESSING STUDIO</small></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="side-label">NGUỒN ẢNH / INPUT</div>',unsafe_allow_html=True)
    st.segmented_control("Nguồn ảnh",["Ảnh mẫu","Tải ảnh lên"],key="source",label_visibility="collapsed",selection_mode="single")
    uploaded=None
    if st.session_state.source=="Tải ảnh lên":
        uploaded=st.file_uploader("Upload Image · PNG / JPEG / WebP",type=["png","jpg","jpeg","webp"],key=f"upload_{st.session_state.upload_epoch}")
        st.caption("Tối đa 15 MB / 25 megapixel. Tự chuyển RGB → grayscale.")
    sample=st.selectbox("Ảnh mẫu",samples,format_func=lambda p:DISPLAY_NAMES.get(p.stem,p.stem),key="sample") if samples else None
    a,b=st.columns(2)
    a.button("↻ Reset",on_click=reset,width="stretch")
    b.button("Nạp ảnh mẫu",on_click=load_sample,width="stretch",disabled=not samples)
    st.markdown('<div class="side-label">KHÁM PHÁ</div>',unsafe_allow_html=True)
    page=st.radio("Điều hướng",PAGES,key="page",label_visibility="collapsed",format_func=lambda p:p)
    st.divider()
    st.toggle("Chế độ trình chiếu",key="presentation")
    st.toggle("Hiện code Python",key="show_code",help="Xem các hàm thực tế của nội dung đang mở, kể cả khi trình chiếu.")
    with st.expander("Tùy chỉnh không gian demo"):
        st.select_slider("Số ảnh tối đa mỗi hàng",options=[1,2,3,4],value=3,key="panel_columns")
        st.slider("Chiều cao ảnh (px)",180,480,300,20,key="panel_height")
        st.toggle("Mở sẵn phần nguyên lý",value=True,key="expand_theory")

if st.session_state.presentation:
    st.markdown('<style>#MainMenu,[data-testid="stToolbar"],footer{display:none!important}h1{font-size:44px!important}.lead,.observation p{font-size:16px}.block-container{max-width:1750px}</style>',unsafe_allow_html=True)

if uploaded is not None and st.session_state.source=="Tải ảnh lên":
    content=uploaded.getvalue()
    source_name=uploaded.name
elif sample:
    content=sample.read_bytes()
    source_name=DISPLAY_NAMES.get(sample.stem,sample.stem)
    if st.session_state.source=="Tải ảnh lên":
        st.info("Chưa có ảnh tải lên. Đang dùng ảnh mẫu để bạn tiếp tục khám phá.")
else:
    st.info("Thêm ảnh vào sample_images hoặc tải ảnh lên ở sidebar để bắt đầu.")
    st.stop()

try:
    rgb,image=read_image(content)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
digest=hashlib.sha256(content).hexdigest()
if st.session_state.get("image_digest")!=digest:
    for key in ("notch_added","notch_applied","benchmark_result","auto_wiener_signature","manual_u","manual_v","notch_fx","notch_fy"):
        st.session_state.pop(key,None)
    st.session_state.image_digest=digest

st.markdown('<div class="topline"><div><strong>TÍCH CHẬP VÀ LỌC ẢNH TRONG MIỀN TẦN SỐ</strong><small>Convolution and Frequency Domain Filtering</small></div><div class="group">Nhóm 1 – 74DCTT24</div></div>',unsafe_allow_html=True)
handlers={"Tổng quan":overview.render,"Convolution Theorem":convolution.render,"Gaussian Blur":lambda img:convolution.render(img,True),
    "HPF – High-pass Filter":frequency.render_hpf,"LPF – Low-pass Filter":frequency.render_lpf,"BPF – Band-pass Filter":frequency.render_bpf,
    "Notch Filter":notch.render,"Image Restoration":restoration.render,"So sánh Convolution":benchmark.render,"Tổng kết":summary.render}
handlers[page](image)
if st.session_state.get("show_code",False):
    from utils.code_view import render_code
    render_code(page)
import html
st.markdown(f'<div class="footnote">FOURIER LAB / {html.escape(source_name)} · {image.shape[1]} × {image.shape[0]} PX</div>',unsafe_allow_html=True)
