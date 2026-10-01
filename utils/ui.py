import base64
import html
from io import BytesIO
import numpy as np
from PIL import Image
from matplotlib import colormaps
import plotly.graph_objects as go
import streamlit as st
from .images import to_png
from .fourier import spectrum, snr


def section(title, subtitle, chapter):
    st.markdown(f'<h1>{title}</h1><p class="lead">{subtitle}</p>', unsafe_allow_html=True)


def observation(text):
    st.markdown(f'<div class="observation"><span>ĐIỀU CẦN QUAN SÁT</span><p>{text}</p></div>', unsafe_allow_html=True)


def theory(text, formula=None):
    with st.expander("Nguyên lý · Theory", expanded=st.session_state.get("expand_theory",not st.session_state.get("presentation", False))):
        st.write(text)
        if formula:
            st.latex(formula)


def image_url(array, kind="image", limit=None):
    values = np.asarray(array, dtype=float)
    if kind == "spectrum":
        maximum = limit if limit is not None else float(np.max(values))
        normalized = values/max(maximum, 1e-12)
        values = colormaps["magma"](np.clip(normalized,0,1))[...,:3]
    elif kind in ("kernel", "mask"):
        maximum = 1.0 if kind == "mask" else max(float(values.max()),1e-12)
        values = colormaps["viridis"](np.clip(values/maximum,0,1))[...,:3]
    elif kind == "signed":
        maximum = max(float(np.abs(values).max()),1e-12)
        values = colormaps["RdBu_r"](np.clip(.5+.5*values/maximum,0,1))[...,:3]
    return "data:image/png;base64,"+base64.b64encode(to_png(values)).decode()


def panel(title, array, subtitle="", kind="image", limit=None):
    url = image_url(array,kind,limit)
    height = st.session_state.get("panel_height",300 if st.session_state.get("presentation",False) else 235)
    st.markdown(f'<div class="image-card"><div class="card-title">{html.escape(title)}</div>'
        f'<div class="image-stage" style="height:{height}px"><img src="{url}" alt="{html.escape(title)}"></div>'
        f'<div class="card-caption">{html.escape(subtitle)}</div></div>', unsafe_allow_html=True)


def panel_row(items):
    count=min(len(items),st.session_state.get("panel_columns",3))
    for start in range(0,len(items),count):
        for col, item in zip(st.columns(min(count,len(items)-start), gap="small"), items[start:start+count]):
            with col:
                panel(*item)


def spectrum_note(maximum=None):
    st.caption("Phổ đã fftshift: tâm = tần số thấp; xa tâm = tần số cao. Màu sáng = biên độ lớn, không phải ảnh sáng hơn. "
               + (f"Các phổ ảnh cùng thang 0–{maximum:.1f}, dùng 20·log₁₀(1+|F|)." if maximum is not None else "Hiển thị 20·log₁₀(1+|F|); mask trắng/sáng = giữ, tối = loại."))


def pipeline(active=-1, animate=False, image=None, result=None):
    labels = [("01", "Ảnh đầu vào", "f(x,y)"), ("02", "Biến đổi Fourier", "DFT"),
              ("03", "Phổ ảnh", "F(u,v)"), ("04", "Nhân với bộ lọc", "× H(u,v)"),
              ("05", "Biến đổi ngược", "IDFT"), ("06", "Ảnh kết quả", "g(x,y)")]
    nodes = "".join(f'<div class="node" id="n{i}"><small>{n}</small><b>{symbol}</b><span>{label}</span></div>' for i,(n,label,symbol) in enumerate(labels))
    previews = ""
    if animate and image is not None:
        previews = f'<div class="previews"><img src="{image_url(image)}" alt="Ảnh gốc"><span id="step">Ảnh đầu vào</span><img id="output" src="{image_url(result)}" alt="Ảnh đầu ra" style="opacity:0"></div>'
    st.iframe(f'''<!doctype html><html><head><style>
    *{{box-sizing:border-box}}body{{margin:0;font-family:Segoe UI,Arial,sans-serif;color:#183a43}}
    .flow{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}}.node{{position:relative;border:1px solid #dae5e5;background:white;border-radius:12px;padding:14px 9px;display:flex;flex-direction:column;gap:8px;min-height:112px}}
    .node small{{color:#8b9ba1;font-size:10px}}.node b{{font-size:20px;letter-spacing:-.5px}}.node span{{font-size:10px;color:#70848b}}
    .node.active{{background:#e1f5eb;border-color:#368772;box-shadow:0 2px 10px #26846b18}}.node.active b{{color:#267969}}
    .previews{{display:flex;justify-content:space-around;align-items:center;margin-top:14px;font-size:13px;color:#267969}}.previews img{{height:140px;max-width:35%;object-fit:contain;border-radius:8px}}
    @media(max-width:600px){{.node{{padding:10px 4px}}.node b{{font-size:14px}}.node span{{font-size:9px}}}}
    </style></head><body><div class="flow">{nodes}</div>{previews}
    <script>let current={0 if animate else active};const running={str(animate).lower()};
    const captions=['Ảnh đầu vào','DFT: chuyển sang miền tần số','Quan sát phổ F(u,v)','Nhân từng phần tử F × H','IDFT: trở về miền không gian','Hoàn tất: ảnh đầu ra'];
    function show(){{document.querySelectorAll('.node').forEach((n,i)=>n.classList.toggle('active',i===current));
    const text=document.getElementById('step');if(text)text.textContent=captions[current];
    if(current===5&&document.getElementById('output'))document.getElementById('output').style.opacity=1;}}
    show();if(running){{const timer=setInterval(()=>{{current++;show();if(current===5)clearInterval(timer)}},850)}}
    </script></body></html>''',height=290 if animate else 125)


def before_after(before, after, left="TRƯỚC XỬ LÝ", right="SAU XỬ LÝ", height=350):
    a,b = image_url(before),image_url(after)
    st.iframe(f'''<!doctype html><html><head><style>
    *{{box-sizing:border-box}}body{{margin:0;font-family:Segoe UI,sans-serif}}.stage{{--split:50%;height:{height-30}px;background:#102631;border-radius:14px;overflow:hidden;position:relative}}
    img{{position:absolute;width:100%;height:100%;object-fit:contain}}.before{{clip-path:inset(0 calc(100% - var(--split)) 0 0)}}
    .line{{position:absolute;left:var(--split);height:100%;width:2px;background:#86d7bb;pointer-events:none}}
    .handle{{position:absolute;left:var(--split);top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#86d7bb;color:#102631;width:38px;height:38px;display:grid;place-items:center;pointer-events:none}}
    .tag{{position:absolute;top:12px;color:#adbcc2;background:#102631ed;border:1px solid #819b9b;border-radius:5px;font-size:10px;padding:7px 10px;pointer-events:none;transition:.15s}}
    .a{{left:12px}}.b{{right:12px}}.active{{color:#c0ffe7;border-color:#86d7bb;box-shadow:0 0 12px #86d7bb60}}
    input{{position:absolute;inset:0;width:100%;height:100%;opacity:0;margin:0;cursor:ew-resize}}p{{text-align:center;font-size:10px;color:#71838d;letter-spacing:1px;margin:8px}}
    </style></head><body><div class="stage" id="stage"><img src="{b}" alt="{html.escape(right)}"><img class="before" src="{a}" alt="{html.escape(left)}"><div class="line"></div><div class="handle">‹ ›</div>
    <span class="tag a">{html.escape(left)}</span><span class="tag b">{html.escape(right)}</span><input id="wipe" type="range" min="0" max="100" value="50" aria-label="So sánh trước và sau"></div><p>KÉO ĐỂ SO SÁNH · PHÍM ← →</p>
    <script>const input=document.getElementById('wipe');function update(){{const v=Number(input.value);document.getElementById('stage').style.setProperty('--split',v+'%');document.querySelector('.a').classList.toggle('active',v>=50);document.querySelector('.b').classList.toggle('active',v<=50)}}input.addEventListener('input',update);update();</script></body></html>''',height=height)


def metrics(reference, observed, restored):
    values = [("SNR trước", snr(reference, observed)),("SNR sau",snr(reference,restored)),
              ("MSE sau",float(np.mean((reference-restored)**2)))]
    for col,(label,value) in zip(st.columns(3),values):
        text = f"{value:.2f} dB" if "SNR" in label else f"{value:.6f}"
        if not np.isfinite(value):
            text = "∞" if value>0 else "Không xác định: ảnh đen"
        col.metric(label,text,border=True)
    st.caption("Đối chiếu với ảnh sạch; đo trên float chưa clip. SNR = 10·log₁₀(Σf² / Σ(f−g)²), không phải PSNR.")


def surface(mask, key):
    stride = max(1, max(mask.shape)//90)
    z = mask[::stride,::stride]
    fig=go.Figure(go.Surface(z=z,colorscale="Viridis",showscale=False))
    fig.update_layout(height=380,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(xaxis_title="u (lấy mẫu)",yaxis_title="v (lấy mẫu)",zaxis_title="|H(u,v)|",camera=dict(eye=dict(x=1.6,y=1.6,z=1.2))))
    st.plotly_chart(fig,width="stretch",key=key,config={"displayModeBar":False})
