from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import numpy as np


class TimeDomainGraph(QWidget):
    def __init__(self, title="Time Domain Graph", parent=None):
        super(TimeDomainGraph, self).__init__(parent)

        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up PyQtGraph plot
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Set plot title
        self.plot_widget.setTitle(title)
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Amplitude")

    def draw_signal(self, linspace, data_points):
        """
        Draws a continuous signal based on linspace and data points.

        :param linspace: np.array of time values.
        :param data_points: np.array of amplitude values corresponding to the linspace.
        """
        # Clear previous plot and draw the new signal
        self.plot_widget.clear()

        # Plot the continuous signal
        self.plot_widget.plot(linspace, data_points, pen='b', name='Signal')

    def draw_samples(self, linspace, sampled_data):
        """
        Draws samples as 'x' markers given linspace and sampled data.

        :param linspace: np.array of time values for sampling.
        :param sampled_data: np.array containing sampled amplitude values.
        """
        # Plot sampled points as "x" markers
        self.plot_widget.plot(linspace, sampled_data, pen=None, symbol='x', symbolSize=10, symbolBrush='r',
                              name='Samples')

    def draw_difference(self, linspace, signal_data1, signal_data2):
        """
        Draws the difference between two signals given linspace and two sets of amplitude values.

        :param linspace: np.array of time values.
        :param signal_data1: np.array containing the first signal amplitude values.
        :param signal_data2: np.array containing the second signal amplitude values.
        """
        if len(signal_data1) != len(signal_data2):
            print("Error: Signal lengths do not match.")
            return

        # Calculate the difference
        difference = signal_data1 - signal_data2

        # Clear previous plots and draw the difference
        self.plot_widget.clear()
        self.plot_widget.plot(linspace, difference, pen='g', name='Difference')