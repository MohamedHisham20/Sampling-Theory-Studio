import pyqtgraph as pg
import numpy as np
from typing import List


class DFTGraph():
    def __init__(self):
        self.DFT_plot_widget = pg.PlotWidget()
        
        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(f)|") #\u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="f", units="HZ")
        self.DFT_plot_widget.plotItem.showGrid(x=True, y=True)

    def draw_DFT_magnitude(self, data_pnts, og_sampling_frequency, reconstruction_sampling_frequency, show_repetitions=False):
        """ plots the discrete fourier transform magnitude using FFT
        """
        self.DFT_plot_widget.plotItem.clear()
        FFT = np.fft.fft(data_pnts)
        fo = np.fft.fftfreq(len(data_pnts), 1/og_sampling_frequency)

        FFT_magnitude = np.abs(FFT)

        magnitude_spectrum = np.abs(FFT)

        # Consider only positive frequencies and find the maximum
        positive_frequencies = fo[:len(fo) // 2]
        positive_magnitude = magnitude_spectrum[:len(magnitude_spectrum) // 2]

        # Find the index of the maximum magnitude
        max_index = np.argmax(positive_magnitude)

        # Get the frequency corresponding to the maximum magnitude
        max_frequency = positive_frequencies[max_index]
        margin_positive = max_frequency * 1.01

        within_margin = np.logical_and(fo >= -margin_positive, fo <= margin_positive)
        filtered_fo = fo[within_margin]
        filtered_FFT_magnitude = FFT_magnitude[within_margin]

        sorted_indices = np.argsort(filtered_fo)
        filtered_fo = filtered_fo[sorted_indices]
        filtered_FFT_magnitude = filtered_FFT_magnitude[sorted_indices]

        # Plot the FFT result within the specified margin
        self.DFT_plot_widget.plotItem.plot(filtered_fo, filtered_FFT_magnitude)

        if show_repetitions:
            impulse_magnitude = max(FFT_magnitude)

            sampling_frequency_impulses_linspace = np.concatenate([
                np.arange(-reconstruction_sampling_frequency / 2, -10, -reconstruction_sampling_frequency),
                np.arange(reconstruction_sampling_frequency / 2, 10, reconstruction_sampling_frequency)
            ])
            positive_sampling_frequency_impulses_linspace = np.arange(-reconstruction_sampling_frequency / 2, 10, reconstruction_sampling_frequency)
            negative_sampling_frequency_impulses_linspace = np.arange(reconstruction_sampling_frequency / 2, -10, -reconstruction_sampling_frequency)

            # for center_freq in sampling_frequency_impulses_linspace:
            #     # Shift the FFT frequency axis by the center frequency
            #     shifted_fo = fo + center_freq
            #     # Plot the repeated FFT magnitude centered at the current frequency
            #     self.DFT_plot_widget.plotItem.plot(shifted_fo, FFT_magnitude,
            #                                        pen='b')  # Using blue for replicas for contrast

            # for center_freq in positive_sampling_frequency_impulses_linspace:
            #     shifted_fo = filtered_fo + center_freq - reconstruction_sampling_frequency / 2
            #     self.DFT_plot_widget.plotItem.plot(shifted_fo, filtered_FFT_magnitude, pen='b')
            #
            # for center_freq in negative_sampling_frequency_impulses_linspace:
            #     shifted_fo = filtered_fo + center_freq + reconstruction_sampling_frequency / 2
            #     self.DFT_plot_widget.plotItem.plot(shifted_fo, filtered_FFT_magnitude, pen='b')

            # for x in sampling_frequency_impulses_linspace:
            #     self.DFT_plot_widget.plotItem.plot([x, x], [0, impulse_magnitude], pen='r')
                