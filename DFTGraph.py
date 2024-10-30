import pyqtgraph as pg
import numpy as np
from PySide6 import QtCore


class DFTGraph():
    def __init__(self):
        self.DFT_plot_widget = pg.PlotWidget()

        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(f)|")  #\u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="f", units="HZ")
        self.DFT_plot_widget.plotItem.showGrid(x=True)
        self.original_pen = pg.mkPen(color='w', width=2)
        self.sampling_frequency_pen = pg.mkPen(color='orange', width=2)
        self.repetition_pen = pg.mkPen(color=(0, 255, 0, 128), width=1, style=QtCore.Qt.DashDotLine)

    def draw_DFT_magnitude(self, data_points, og_sampling_period, reconstruction_sampling_frequency,
                           show_repetitions=False):
        """ plots the discrete fourier transform magnitude using FFT
        """
        self.DFT_plot_widget.plotItem.clear()

        FFT_magnitude, frequency_bins = self.compute_FFT(data_points, og_sampling_period)

        sampling_frequency_impulses_magnitude = max(FFT_magnitude) * 5
        sampling_frequency_impulses = (
            np.repeat(sampling_frequency_impulses_magnitude, 2),
            [-reconstruction_sampling_frequency / 2, reconstruction_sampling_frequency / 2]
        )
        self.draw_impulses(*sampling_frequency_impulses, pen=self.sampling_frequency_pen)

        self.draw_impulses(FFT_magnitude, frequency_bins, self.original_pen)

        if show_repetitions:
            repeated_frequencies = []
            repeated_magnitudes = []

            # Iterate through original frequencies and repeat them
            for freq, magnitude in zip(frequency_bins, FFT_magnitude):
                if magnitude > 20:  # Only consider significant magnitudes
                    # Repeat frequency three times at intervals of sampling frequency
                    for n in range(-2, 3):  # Repeat around the original frequency
                        repeated_frequencies.append(freq + n * reconstruction_sampling_frequency)
                        repeated_magnitudes.append(magnitude)

            # Draw the perceived repetitions with the repetition pen
            self.draw_impulses(repeated_magnitudes, repeated_frequencies, self.repetition_pen)

    def compute_FFT(self, data_points, og_sampling_period):
        fft = np.fft.fft(data_points)
        frequency_bins = np.fft.fftfreq(len(data_points), og_sampling_period)

        magnitude = np.abs(fft)

        above_threshold = magnitude > 5
        filtered_magnitudes = magnitude[above_threshold]
        filtered_frequencies = frequency_bins[above_threshold]
        return filtered_magnitudes, filtered_frequencies

    def draw_impulses(self, magnitudes, frequencies, pen):
        if pen == self.original_pen:
            name = "Original Signal Components"
        elif pen == self.repetition_pen:
            name = "Perceived Repetition"
        else:
            name = "Sampling Frequency"

        x_data = np.repeat(frequencies, 3)
        y_data = np.zeros_like(x_data)
        y_data[1::3] = magnitudes

        impulse_item = pg.PlotDataItem(x=x_data, y=y_data, pen=pen)
        self.DFT_plot_widget.addItem(impulse_item)
