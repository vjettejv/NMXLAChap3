import unittest
from io import BytesIO
import numpy as np
from PIL import Image
from scipy.signal import convolve,fftconvolve
from utils.fourier import fft_image,spectrum,linear_fft_convolve,psf_to_otf,apply_mask,snr
from utils.filters import gaussian_kernel,ideal_mask,gaussian_lpf,dog_kernel,periodic_noise,notch_mask,detect_peaks
from utils.restoration import degrade,inverse_filter,wiener_filter,automatic_wiener
from utils.benchmark import benchmark
from utils.images import normalize,read_image


class NumericalTests(unittest.TestCase):
    def setUp(self):
        self.image=np.random.default_rng(7).random((65,80))

    def test_fft_round_trip_and_zero_spectrum(self):
        np.testing.assert_allclose(np.fft.ifft2(fft_image(self.image)).real,self.image,atol=1e-14)
        self.assertTrue(np.isfinite(spectrum(fft_image(np.zeros((20,20))))).all())

    def test_linear_fft_matches_direct_odd_rectangular(self):
        for shape in ((65,80),(64,64)):
            image=np.random.default_rng(2).random(shape)
            for size in (3,11,51):
                k=gaussian_kernel(size,2.)
                actual,*_=linear_fft_convolve(image,k)
                expected=convolve(image,k,mode="same",method="direct")
                np.testing.assert_allclose(actual,expected,atol=2e-14)

    def test_psf_origin_no_one_pixel_shift(self):
        impulse=np.zeros((5,5)); impulse[2,2]=1
        for shape in ((65,80),(64,65)):
            np.testing.assert_allclose(psf_to_otf(impulse,shape),1,atol=1e-14)

    def test_gaussian_normalization_and_dog_dc(self):
        self.assertAlmostEqual(gaussian_kernel(51,6).sum(),1)
        self.assertAlmostEqual(dog_kernel(51,1.5,4).sum(),0)
        with self.assertRaises(ValueError): dog_kernel(51,4,1)

    def test_lpf_hpf_complement_and_real_output(self):
        for shape in ((65,80),(64,64)):
            image=np.random.default_rng(4).random(shape)
            low=ideal_mask(shape,15)
            high=ideal_mask(shape,15,True)
            np.testing.assert_array_equal(low+high,1)
            a,_,_=apply_mask(image,low); b,_,_=apply_mask(image,high)
            np.testing.assert_allclose(a+b,image,atol=1e-14)
            f=np.fft.fftshift(fft_image(image))
            self.assertLess(np.abs(np.fft.ifft2(np.fft.ifftshift(f*high)).imag).max(),1e-14)

    def test_gaussian_lpf_constant_image(self):
        result,*_=gaussian_lpf(np.full((65,80),.4),5)
        np.testing.assert_allclose(result,.4,atol=1e-14)

    def test_notch_removes_sinusoid_and_preserves_real(self):
        for shape in ((65,80),(64,64)):
            original=np.full(shape,.5)
            noisy=periodic_noise(original,12,9,.2)
            peaks=detect_peaks(noisy)
            self.assertEqual(peaks[0][:2],(12,9))
            mask=notch_mask(shape,12,9,1)
            result,_,_=apply_mask(noisy,mask)
            np.testing.assert_allclose(result,original,atol=1e-13)
            raw=np.fft.ifft2(fft_image(noisy)*np.fft.ifftshift(mask))
            self.assertLess(np.abs(raw.imag).max(),1e-14)

    def test_inverse_recovers_and_wiener_regularizes_noise(self):
        y,x=np.indices((64,64))
        image=.5+.2*np.sin(x/5)+.1*np.cos(y/8)
        kernel=gaussian_kernel(11,1.2)
        observed,_,h=degrade(image,kernel,0.)
        recovered=inverse_filter(observed,h,1e-6)
        self.assertLess(np.mean((image-recovered)**2),np.mean((image-observed)**2))
        noisy,_,h=degrade(image,kernel,.025)
        recovered=wiener_filter(noisy,h,.01)
        self.assertTrue(np.isfinite(recovered).all())
        unstable=inverse_filter(noisy,h,1e-6)
        self.assertLess(np.mean((image-recovered)**2),np.mean((image-unstable)**2))
        # A Wiener filter is not guaranteed to beat every observed image for an
        # arbitrary K. Verify the exact identity-PSF response independently.
        np.testing.assert_allclose(wiener_filter(noisy,np.ones(noisy.shape),.1),noisy/1.1,atol=1e-14)

    def test_unsupervised_wiener_output(self):
        small=self.image[:32,:32]
        kernel=gaussian_kernel(5,1)
        observed,*_=degrade(small,kernel,.01)
        result=automatic_wiener(observed,kernel)
        self.assertEqual(result.shape,small.shape)
        self.assertTrue(np.isfinite(result).all())

    def test_snr_known_cases(self):
        self.assertEqual(snr(np.ones((3,3)),np.zeros((3,3))),0)
        self.assertTrue(np.isposinf(snr(self.image,self.image)))
        self.assertTrue(np.isneginf(snr(np.zeros((3,3)),np.ones((3,3)))))

    def test_benchmark_same_output_and_repeats(self):
        outputs,times,error=benchmark(self.image[:20,:20],gaussian_kernel(3,1),10)
        self.assertLess(error,1e-13)
        self.assertTrue(all(len(x)==10 and min(x)>0 for x in times.values()))

    def test_upload_types_and_invalid_files(self):
        for mode in ("RGB","RGBA","L","P"):
            rgb,gray=normalize(Image.new(mode,(800,600)))
            self.assertEqual(gray.shape,(288,384))
            self.assertEqual(rgb.shape,(288,384,3))
            self.assertTrue(np.isfinite(gray).all())
        for size in ((2,2),(12000,80)):
            with self.assertRaises(ValueError): normalize(Image.new("RGB",size))
        with self.assertRaises(ValueError): read_image(b"not an image")


if __name__=="__main__": unittest.main()
