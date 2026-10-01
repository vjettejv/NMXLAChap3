from io import BytesIO
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
from skimage.color import rgb2gray
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "sample_images"
DISPLAY_NAMES = {"cameraman": "Cameraman · Đường biên", "coffee": "Coffee · Chi tiết bề mặt",
    "astronaut": "Astronaut · Chân dung", "patterns": "Patterns · Tần số tổng hợp", "chelsea": "Chelsea · Texture",
    "lena": "Lena", "mandrill": "Mandrill", "parrot": "Parrot", "rhino": "Rhino"}


def available_samples():
    return sorted([p for p in SAMPLE_DIR.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")],
                  key=lambda p: (p.stem != "cameraman", p.name))


def normalize(image, max_side=384):
    if image.width*image.height > 25_000_000:
        raise ValueError("Ảnh vượt 25 megapixel. Hãy thu nhỏ ảnh trước khi tải lên.")
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255,255,255,255))
        image = Image.alpha_composite(bg, rgba).convert("RGB")
    elif image.mode in ("I", "F") or image.mode.startswith("I;16"):
        raise ValueError("Hãy chuyển ảnh 16-bit/float sang PNG hoặc JPEG 8-bit trước khi tải.")
    else:
        image = image.convert("RGB")
    image.thumbnail((max_side,max_side), Image.Resampling.LANCZOS)
    if min(image.size) < 64:
        raise ValueError("Cạnh ngắn của ảnh sau thu nhỏ cần ≥ 64 px để hỗ trợ kernel 51×51.")
    rgb = np.asarray(image, dtype=np.float64)/255
    return rgb, rgb2gray(rgb)


@st.cache_data(show_spinner=False, max_entries=12)
def read_image(data, max_side=384):
    try:
        with Image.open(BytesIO(data)) as image:
            return normalize(image, max_side)
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("Không đọc được ảnh. Vui lòng chọn PNG, JPEG hoặc WebP hợp lệ.") from exc


def to_png(image):
    data = np.rint(np.clip(image,0,1)*255).astype(np.uint8)
    stream = BytesIO()
    Image.fromarray(data).save(stream, format="PNG")
    return stream.getvalue()
