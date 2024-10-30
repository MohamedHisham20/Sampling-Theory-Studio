import pyqtgraph as pg
import numpy as np
from PySide6 import QtCore


class DFTGraph():
    def __init__(self):
        self.DFT_plot_widget = pg.PlotWidget()

        # Add legend to the plot
        self.legend = pg.LegendItem(offset=(-10, 2))  # Adjust offset as needed
        self.legend.setParentItem(self.DFT_plot_widget.plotItem)  # Set the legend as a child of the plot item
        self.legend.hide()

        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(f)|")  # \u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="f", units="HZ")
        self.DFT_plot_widget.plotItem.showGrid(x=True)

        # Define pens
        self.original_pen = pg.mkPen(color='w', width=2)
        self.sampling_frequency_pen = pg.mkPen(color='orange', width=2)
        self.repetition_pen = pg.mkPen(color=(0, 255, 0, 128), width=1, style=QtCore.Qt.DashDotLine)

    def draw_DFT_magnitude(self, data_points, og_sampling_period, reconstruction_sampling_frequency,
                           show_repetitions=False):
        """Plots the discrete fourier transform magnitude using FFT."""
        self.DFT_plot_widget.plotItem.clear()
        self.legend.clear()

        FFT_magnitude, frequency_bins = self.compute_FFT(data_points, og_sampling_period)

        # Draw sampling frequency impulses
        sampling_frequency_impulses_magnitude = max(FFT_magnitude) * 5
        sampling_frequency_impulses = [-reconstruction_sampling_frequency / 2, reconstruction_sampling_frequency / 2]
        sampling_frequency_to_plot = []
        sampling_magnitude_to_plot = []
        if show_repetitions:
            for freq in sampling_frequency_impulses:
                for n in range(-2, 3):  # Repeat around the sampling frequency
                    sampling_frequency_to_plot.append(freq + n * reconstruction_sampling_frequency)
                    sampling_magnitude_to_plot.append(sampling_frequency_impulses_magnitude)
        else:
            sampling_frequency_to_plot = sampling_frequency_impulses
            sampling_magnitude_to_plot = [sampling_frequency_impulses_magnitude, sampling_frequency_impulses_magnitude]
        self.draw_impulses(sampling_magnitude_to_plot, sampling_frequency_to_plot, pen=self.sampling_frequency_pen)

        # Draw original signal components
        self.draw_impulses(FFT_magnitude, frequency_bins, self.original_pen)

        # Show repetitions if requested
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

            # Draw perceived repetitions
            self.draw_impulses(repeated_magnitudes, repeated_frequencies, self.repetition_pen)

        # Show the legend
        self.legend.show()

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

        # Create impulse data for drawing
        x_data = np.repeat(frequencies, 3)
        y_data = np.zeros_like(x_data)
        y_data[1::3] = magnitudes

        impulse_item = pg.PlotDataItem(x=x_data, y=y_data, pen=pen)

        # Add item to the plot
        self.DFT_plot_widget.addItem(impulse_item)

        # Add item to the legend
        self.legend.addItem(impulse_item, name)
