import numpy as np
from scipy.interpolate import interp1d, lagrange, CubicSpline


class SignalReconstruction:
    ZERO_ORDER_HOLD = 1000
    LINEAR = 1001
    NYQUIST = 1002
    CUBIC_SPLINE = 1003
    FOURIER = 1004
    NEAREST_NEIGHBOR = 1005

    def __init__(self, samples, sampling_frequency, timespace):
        self.samples = samples
        self.sampling_frequency = sampling_frequency
        self.timespace = timespace

        self.sampling_period = 1 / self.sampling_frequency
        self.sample_times = np.arange(self.timespace[0], self.timespace[-1], self.sampling_period)

        self.interpolation_function = None

    @staticmethod
    def sinc(x):
        """Compute the sinc function."""
        small_value_threshold = 1e-10  # Set a small threshold to handle values near zero
        x = np.where(np.abs(x) < small_value_threshold, small_value_threshold, x)
        return np.sin(np.pi * x) / (np.pi * x)


    def reconstruct_signal(self, method=NYQUIST):
        """
        Reconstructs the signal using the selected technique.

        :return: np.array containing the reconstructed signal.
        """
        if method == SignalReconstruction.ZERO_ORDER_HOLD:
            self.interpolation_function = self.zero_order_hold
        elif method == SignalReconstruction.LINEAR:
            self.interpolation_function = self.linear_interpolation
        elif method == SignalReconstruction.NYQUIST:
            self.interpolation_function = self.nyquist_interpolation
        elif method == SignalReconstruction.CUBIC_SPLINE:
            self.interpolation_function = self.cubic_spline_interpolation
        elif method == SignalReconstruction.FOURIER:
            self.interpolation_function = self.fourier_series_interpolation
        elif method == SignalReconstruction.NEAREST_NEIGHBOR:
            self.interpolation_function = self.nearest_neighbor_interpolation
        return self.interpolation_function()

    def nyquist_interpolation(self):
        """
        Reconstruct the signal using Nyquist interpolation (sinc function).

        :param samples: np.array containing the sampled data points.
        :param sampling_frequency: int representing the sampling frequency.
        :return: np.array containing the reconstructed signal.
        """
        reconstructed = np.zeros_like(self.timespace)
        for i in range(len(self.samples)):
            reconstructed += self.samples[i] * SignalReconstruction.sinc((self.timespace - self.sample_times[i]) / self.sampling_period)
        return reconstructed

    def fourier_series_interpolation(self):
        """
        Reconstruct the signal using Fourier series interpolation.

        :param samples: np.array containing the sampled data points.
        :param sampling_frequency: int representing the sampling frequency.
        :return: np.array containing the reconstructed signal.
        """
        # Get the first few Fourier coefficients
        fft_coeffs = np.fft.fft(self.samples)

        # Reconstruct the signal using the inverse Fourier transform
        reconstructed = np.fft.ifft(fft_coeffs)

        # Interpolate the reconstructed signal to match the timespace
        reconstructed = np.interp(self.timespace, np.linspace(self.timespace[0], self.timespace[-1], len(reconstructed)), np.real(reconstructed))
        return reconstructed

    def zero_order_hold(self):
        indices = np.searchsorted(self.sample_times, self.timespace) - 1
        indices = np.clip(indices, 0, len(self.samples) - 1)  # Ensure valid index range
        return self.samples[indices]

    def linear_interpolation(self):
        linear_interp = interp1d(self.sample_times, self.samples, kind='linear', fill_value="extrapolate")
        return linear_interp(self.timespace)

    def polynomial_interpolation(self):
        poly = lagrange(self.sample_times, self.samples)
        return poly(self.timespace)

    def cubic_spline_interpolation(self):
        spline = CubicSpline(self.sample_times, self.samples)
        return spline(self.timespace)

    def nearest_neighbor_interpolation(self):
        indices = np.argmin(np.abs(self.sample_times[:, np.newaxis] - self.timespace), axis=0)
        indices = np.clip(indices, 0, len(self.samples) - 1)  # Ensure valid index range
        return self.samples[indices]
