"""Float64 Fourier operations; keep signed values and phase until display."""
import numpy as np


def fft_image(image):
    return np.fft.fft2(np.asarray(image, dtype=np.float64))


def spectrum(transform):
    return 20 * np.log10(1 + np.abs(np.fft.fftshift(transform)))


def frequency_grid(shape):
    y = np.fft.fftshift(np.fft.fftfreq(shape[0])) * shape[0]
    x = np.fft.fftshift(np.fft.fftfreq(shape[1])) * shape[1]
    return np.meshgrid(x, y)


def apply_mask(image, shifted_mask):
    transform = fft_image(image)
    filtered = np.fft.fftshift(transform) * shifted_mask
    result = np.fft.ifft2(np.fft.ifftshift(filtered))
    return result.real, transform, np.fft.ifftshift(filtered)


def psf_to_otf(kernel, shape):
    """Put the PSF origin at (0,0) before FFT, including for odd image sizes."""
    if any(k > s for k, s in zip(kernel.shape, shape)):
        raise ValueError("Kernel không được lớn hơn ảnh.")
    padded = np.zeros(shape, dtype=np.float64)
    padded[:kernel.shape[0], :kernel.shape[1]] = kernel
    padded = np.roll(padded, (-(kernel.shape[0] // 2), -(kernel.shape[1] // 2)), axis=(0, 1))
    return fft_image(padded)


def linear_fft_convolve(image, kernel):
    """Zero-pad to M+K-1,N+L-1; same crop matches scipy.signal.convolve."""
    shape = tuple(np.array(image.shape) + np.array(kernel.shape) - 1)
    f = np.fft.fft2(image, s=shape)
    h = np.fft.fft2(kernel, s=shape)
    g = f * h
    full = np.fft.ifft2(g).real
    y, x = (np.array(kernel.shape) - 1) // 2
    return full[y:y+image.shape[0], x:x+image.shape[1]], f, h, g


def snr(reference, output):
    signal = float(np.sum(np.square(reference, dtype=np.float64)))
    error = float(np.sum(np.square(reference - output, dtype=np.float64)))
    if error == 0:
        return float("inf")
    if signal == 0:
        return float("-inf")
    return float(10 * np.log10(signal / error))
