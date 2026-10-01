import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]


class AppTests(unittest.TestCase):
    def app(self):
        app=AppTest.from_file(str(ROOT/"app.py"),default_timeout=45).run()
        self.assertFalse(app.exception)
        return app

    def navigate(self,app,page):
        app.radio(key="page").set_value(page).run()
        self.assertFalse(app.exception)

    def test_all_pages(self):
        app=self.app()
        for page in ["Convolution Theorem","Gaussian Blur","HPF – High-pass Filter","LPF – Low-pass Filter",
                     "BPF – Band-pass Filter","Notch Filter","Image Restoration","So sánh Convolution","Tổng kết"]:
            self.navigate(app,page)

    def test_code_and_flexible_layout(self):
        app=self.app()
        app.toggle(key="show_code").set_value(True).run()
        app.toggle(key="presentation").set_value(True).run()
        for page in ["Tổng quan","Convolution Theorem","Gaussian Blur","HPF – High-pass Filter","LPF – Low-pass Filter",
                     "BPF – Band-pass Filter","Notch Filter","Image Restoration","So sánh Convolution","Tổng kết"]:
            self.navigate(app,page)
            self.assertGreater(len(app.code),0)
        app.select_slider(key="panel_columns").set_value(1).run()
        app.slider(key="panel_height").set_value(400).run()
        self.assertFalse(app.exception)
        app.toggle(key="show_code").set_value(False).run()
        self.assertEqual(len(app.code),0)

    def test_notch_and_restoration_controls(self):
        app=self.app(); self.navigate(app,"Notch Filter")
        next(b for b in app.button if "Add Periodic Noise" in b.label).click().run()
        self.assertFalse(app.exception)
        next(b for b in app.button if "Áp dụng Notch" in b.label).click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric),3)
        self.navigate(app,"Image Restoration")
        app.toggle(key="inverse_noise").set_value(True).run()
        self.assertFalse(app.exception)
        app.radio(key="wiener_method").set_value("Unsupervised Wiener · scikit-image").run()
        next(b for b in app.button if b.label=="Chạy Unsupervised Wiener").click().run()
        self.assertFalse(app.exception)

    def test_gaussian_hpf_lpf_and_invalid_dog(self):
        app=self.app(); self.navigate(app,"Gaussian Blur")
        app.select_slider(key="gaussian_size").set_value(51).run()
        app.slider(key="gaussian_sigma").set_value(15.).run()
        self.assertFalse(app.exception)
        self.navigate(app,"HPF – High-pass Filter")
        app.toggle(key="hpf_enhance").set_value(True).run()
        self.assertFalse(app.exception)
        self.navigate(app,"LPF – Low-pass Filter")
        app.segmented_control(key="lpf_mode").set_value("Gaussian LPF").run()
        self.assertFalse(app.exception)
        self.navigate(app,"BPF – Band-pass Filter")
        app.slider(key="dog_s1").set_value(8.).run()
        self.assertFalse(app.exception)
        self.assertTrue(app.warning)

    def test_benchmark_and_reset(self):
        app=self.app(); self.navigate(app,"So sánh Convolution")
        next(b for b in app.button if "Run Benchmark" in b.label).click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.success)
        next(b for b in app.button if b.label=="↻ Reset").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["page"],"Tổng quan")

    def test_presentation_and_source_change(self):
        app=self.app()
        app.toggle(key="presentation").set_value(True).run()
        self.navigate(app,"Image Restoration")
        self.assertFalse(app.exception)
        self.assertFalse(any(r.key=="wiener_method" for r in app.radio))
        self.navigate(app,"Convolution Theorem")
        next(b for b in app.button if "Minh họa từng bước" in b.label).click().run()
        self.assertFalse(app.exception)


if __name__=="__main__": unittest.main()

