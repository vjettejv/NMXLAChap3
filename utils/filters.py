import numpy as np
from scipy import ndimage
from .fourier import fft_image, frequency_grid, apply_mask


def gaussian_kernel(size=21, sigma=3.0):
    if size < 3 or size % 2 == 0 or sigma <= 0:
        raise ValueError("Kernel phải lẻ ≥ 3; sigma > 0.")
    axis = np.arange(size, dtype=float) - size // 2
    x, y = np.meshgrid(axis, axis)
    kernel = np.exp(-(x*x+y*y)/(2*sigma*sigma))
    return kernel / kernel.sum()


def ideal_mask(shape, cutoff, highpass=False):
    x, y = frequency_grid(shape)
    low = (x*x+y*y <= cutoff*cutoff).astype(float)
    return 1-low if highpass else low


def gaussian_lpf(image, sigma):
    f = fft_image(image)
    g = ndimage.fourier_gaussian(f, sigma=sigma)
    h = ndimage.fourier_gaussian(np.ones(image.shape, dtype=complex), sigma=sigma).real
    return np.fft.ifft2(g).real, f, g, np.fft.fftshift(h)


def dog_kernel(size, sigma1, sigma2):
    if not 0 < sigma1 < sigma2:
        raise ValueError("Cần sigma 1 < sigma 2.")
    return gaussian_kernel(size, sigma1) - gaussian_kernel(size, sigma2)


def periodic_noise(image, fx=32, fy=12, strength=0.2):
    y, x = np.indices(image.shape)
    wave = strength * np.sin(2*np.pi*(fx*x/image.shape[1] + fy*y/image.shape[0]))
    # No clipping before FFT: clipping would introduce harmonics.
    return image + wave


def notch_mask(shape, fx, fy, radius=2.0):
    x, y = frequency_grid(shape)
    h, w = shape
    mask = np.ones(shape)
    for px, py in ((fx, fy), (-fx, -fy)):
        dx = (x-px+w/2) % w - w/2
        dy = (y-py+h/2) % h - h/2
        mask[dx*dx+dy*dy <= radius*radius] = 0
    return mask


def detect_peaks(image, count=6):
    """Candidate conjugate pairs detected from the noisy image, not its reference."""
    mag = np.abs(np.fft.fftshift(fft_image(image)))
    x, y = frequency_grid(image.shape)
    candidates = (mag == ndimage.maximum_filter(mag, size=5, mode="wrap"))
    candidates &= x*x+y*y > 8**2
    candidates &= (y > 0) | ((y == 0) & (x > 0))
    indices = np.argwhere(candidates)
    indices = sorted(indices, key=lambda p: mag[tuple(p)], reverse=True)[:count]
    return [(int(round(x[a,b])), int(round(y[a,b])), float(mag[a,b])) for a,b in indices]
