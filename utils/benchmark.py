from time import perf_counter_ns
import numpy as np
from scipy.signal import convolve, fftconvolve


def benchmark(image, kernel, repeats=10, progress=None):
    if not 10 <= repeats <= 100:
        raise ValueError("Số lần lặp phải trong khoảng 10–100.")
    methods = {"convolve · direct": lambda: convolve(image, kernel, mode="same", method="direct"),
               "fftconvolve": lambda: fftconvolve(image, kernel, mode="same")}
    outputs = {name: function() for name,function in methods.items()}
    times = {name: [] for name in methods}
    names = list(methods)
    for i in range(repeats):
        for name in names if i % 2 == 0 else names[::-1]:
            start = perf_counter_ns()
            methods[name]()
            times[name].append((perf_counter_ns()-start)/1e6)
        if progress:
            progress((i+1)/repeats)
    error = float(np.max(np.abs(outputs[names[0]] - outputs[names[1]])))
    return outputs, times, error
