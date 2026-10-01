"""Read-only source explorer, using the actual numerical implementation."""
import inspect
import streamlit as st
from . import fourier, filters, restoration, benchmark


def render_code(page):
    common=[fourier.fft_image,fourier.spectrum,fourier.frequency_grid,fourier.apply_mask]
    groups={
        "Tổng quan":common,
        "Convolution Theorem":[filters.gaussian_kernel,fourier.linear_fft_convolve],
        "Gaussian Blur":[filters.gaussian_kernel,fourier.linear_fft_convolve,filters.gaussian_lpf],
        "HPF – High-pass Filter":[filters.ideal_mask,fourier.frequency_grid,fourier.apply_mask,fourier.snr],
        "LPF – Low-pass Filter":[filters.ideal_mask,filters.gaussian_lpf,fourier.apply_mask],
        "BPF – Band-pass Filter":[filters.dog_kernel,filters.gaussian_kernel,fourier.linear_fft_convolve],
        "Notch Filter":[filters.periodic_noise,filters.detect_peaks,filters.notch_mask,fourier.apply_mask],
        "Image Restoration":[restoration.degrade,fourier.psf_to_otf,restoration.inverse_filter,restoration.wiener_filter,restoration.automatic_wiener],
        "So sánh Convolution":[fn for _,fn in inspect.getmembers(benchmark,inspect.isfunction) if fn.__module__==benchmark.__name__],
        "Tổng kết":common+[filters.gaussian_kernel,filters.notch_mask,restoration.wiener_filter],
    }
    functions=groups.get(page,common)
    st.divider()
    st.markdown("### Code Python · Cách triển khai")
    st.caption("Mã nguồn thực tế đang dùng trong demo. Các hàm có thể gọi hàm hỗ trợ trong utils; đây là phần xem code, không phải trình chạy code độc lập.")
    names=[fn.__name__ for fn in functions]
    selected=st.selectbox("Chọn bước xử lý để xem",names,key="code_step_"+page)
    fn=functions[names.index(selected)]
    source=inspect.getsource(fn)
    st.caption(f"{fn.__module__.replace('.', '/')}.py → {selected}")
    st.code(source,language="python",line_numbers=True,wrap_lines=True)
    with st.expander("Xem toàn bộ các hàm của mục này"):
        for item in functions:
            st.markdown(f"**{item.__name__}**")
            st.code(inspect.getsource(item),language="python",line_numbers=True,wrap_lines=True)
