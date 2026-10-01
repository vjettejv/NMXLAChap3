import numpy as np
from skimage.restoration import unsupervised_wiener
from .fourier import fft_image, psf_to_otf


def degrade(image, kernel, noise_sigma=0.0, seed=42):
    h = psf_to_otf(kernel, image.shape)
    blurred = np.fft.ifft2(fft_image(image)*h).real
    observed = blurred + np.random.default_rng(seed).normal(0, noise_sigma, image.shape)
    return observed, blurred, h


def inverse_filter(observed, h, epsilon=0.001):
    if epsilon <= 0:
        raise ValueError("Epsilon phải dương.")
    denominator = h + epsilon
    # Guard the rare H == -epsilon cancellation of a finite, truncated PSF.
    floor = max(np.finfo(float).eps, epsilon*1e-6)
    denominator = np.where(np.abs(denominator) < floor, floor*np.exp(1j*np.angle(denominator)), denominator)
    return np.fft.ifft2(fft_image(observed)/denominator).real


def wiener_filter(observed, h, balance=0.01):
    if balance <= 0:
        raise ValueError("K phải dương.")
    return np.fft.ifft2(np.conj(h)*fft_image(observed)/(np.abs(h)**2+balance)).real


def automatic_wiener(observed, kernel):
    # Same periodic boundary convention as the forward degradation model.
    restored, _ = unsupervised_wiener(observed, kernel, clip=False, rng=42,
        user_params={"min_num_iter": 15, "max_num_iter": 50})
    return restored
