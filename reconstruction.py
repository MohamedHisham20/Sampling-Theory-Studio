import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt
from scipy.interpolate import interp1d, lagrange, CubicSpline


class Reconstruction(QWidget):
    def __init__(self):
        super(Reconstruction, self).__init__()
        self.setWindowTitle("Signal Reconstruction")
        self.setGeometry(100, 100, 800, 600)

        # Layout setup
        layout = QVBoxLayout()

        # PyQtGraph widget for plotting
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Generate sample data
        self.sample_times = np.linspace(0, 9, 10)
        print("sample times: ", self.sample_times)
        self.samples = np.sin(self.sample_times)
        self.t = np.linspace(0, 9.9, 100)
        print("t values: ", self.t)

        # Initial plot of sample data points only without lines in between
        self.plot_widget.plot(self.sample_times, self.samples, pen=None, symbol='o', symbolBrush='r',
                              name="Original Samples")

        # Label for selection
        self.label = QLabel("Select a reconstruction technique:")
        layout.addWidget(self.label)

        # ComboBox for technique selection
        self.combo = QComboBox()
        techniques = [
            "Zero-order hold", "Linear interpolation", "Sinc interpolation",
            "Nyquist interpolation", "Polynomial interpolation",
            "Cubic spline interpolation", "Fourier series interpolation",
            "Nearest neighbor interpolation"
        ]
        self.combo.addItems(techniques)
        layout.addWidget(self.combo)

        # Button to reconstruct signal
        self.button = QPushButton("Reconstruct Signal")
        layout.addWidget(self.button)

        # Set layout
        self.setLayout(layout)

        # Connect the button to the reconstruction method
        self.button.clicked.connect(self.reconstruct_signal)

    def reconstruct_signal(self):
        # Clear previous plot
        self.plot_widget.clear()

        # Re-plot original samples
        self.plot_widget.plot(self.sample_times, self.samples, pen=None, symbol='o', symbolBrush='r',
                              name="Original Samples")

        # Get selected reconstruction technique
        technique = self.combo.currentText()

        # Reconstruct signal based on selected technique
        try:
            if technique == "Zero-order hold":
                reconstructed = self.zero_order_hold(self.sample_times, self.samples, self.t)
            elif technique == "Linear interpolation":
                reconstructed = self.linear_interpolation(self.sample_times, self.samples, self.t)
            elif technique == "Sinc interpolation":
                reconstructed = self.sinc_interpolation(self.sample_times, self.samples, self.t)
            elif technique == "Nyquist interpolation":
                reconstructed = self.nyquist_interpolation(self.samples, self.sample_times, t=self.t)
            elif technique == "Polynomial interpolation":
                reconstructed = self.polynomial_interpolation(self.sample_times, self.samples, self.t)
            elif technique == "Cubic spline interpolation":
                reconstructed = self.spline_interpolation(self.sample_times, self.samples, self.t)
            elif technique == "Fourier series interpolation":
                reconstructed = self.fourier_series_interpolation(self.samples, 10, self.t, T=10)
            elif technique == "Nearest neighbor interpolation":
                reconstructed = self.nearest_neighbor_interpolation(self.sample_times, self.samples, self.t)

            # Plot reconstructed signals
            self.plot_widget.plot(self.t, reconstructed, pen='b', name="Reconstructed Signal")

        except Exception as e:
            print(f"Error in {technique}: {e}")

    def zero_order_hold(self, sample_times, samples, t):
        indices = np.searchsorted(sample_times, t) - 1
        indices = np.clip(indices, 0, len(samples) - 1)  # Ensure valid index range
        return samples[indices]

    def linear_interpolation(self, sample_times, samples, t):
        linear_interp = interp1d(sample_times, samples, kind='linear', fill_value="extrapolate")
        return linear_interp(t)

    def sinc_interpolation(self, sample_times, samples, t):
        sinc_matrix = np.tile(t, (len(sample_times), 1)) - np.tile(sample_times[:, np.newaxis], (1, len(t)))
        return np.dot(samples, np.sinc(sinc_matrix))

    def sinc(self, x):
        """Compute the sinc function."""
        return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

    def nyquist_interpolation(self, samples, sample_times, t):
        """Reconstruct the signal using Nyquist interpolation (sinc function)."""
        reconstructed = np.zeros_like(t)
        for n in range(len(samples)):
            # Calculate the contribution of each sample using the sinc function
            reconstructed += samples[n] * self.sinc((t - sample_times[n]) / (sample_times[1] - sample_times[0]))
        return reconstructed

    # create nyquist interpolation function from the equation
    def nyquist_interpolation_2(self, samples, t_s, t):
        z = 0
        Ns = len(self.samples)
        fs = 1 / (self.sample_times[1] - self.sample_times[0])
        Ts = 1 / fs
        for i in range(-int((Ns - 1) / 2), int((Ns - 1) / 2), 1):
            n = int(i + (Ns - 1) / 2 + 1)
            denominator = np.pi * fs * (t - i * Ts)
            z += self.samples[n] * np.where(denominator == 0, 1, np.sin(denominator) / denominator)
        return z

    def polynomial_interpolation(self, sample_times, samples, t):
        poly = lagrange(sample_times, samples)
        return poly(t)

    def spline_interpolation(self, sample_times, samples, t):
        spline = CubicSpline(sample_times, samples)
        return spline(t)

    def fourier_series_interpolation(self, samples, num_components, t, T=1.0):
        n = len(samples)
        fft_coeffs = np.fft.fft(samples)[:num_components]  # Get first few Fourier coefficients
        reconstructed = np.zeros_like(t, dtype=np.complex128)  # Use complex128 for reconstruction

        for k in range(num_components):
            frequency = 2 * np.pi * k / T
            reconstructed += fft_coeffs[k] * np.exp(1j * frequency * t)

        return np.real(reconstructed)  # Return the real part of the reconstruction

    def nearest_neighbor_interpolation(self, sample_times, samples, t):
        indices = np.argmin(np.abs(sample_times[:, np.newaxis] - t), axis=0)
        indices = np.clip(indices, 0, len(samples) - 1)  # Ensure valid index range
        return samples[indices]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Reconstruction()
    window.show()
    sys.exit(app.exec_())
