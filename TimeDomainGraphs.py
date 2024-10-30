from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class TimeDomainGraphs:
    def __init__(self):
        # Set up three PyQtGraph plot widgets
        self.signal_plot = pg.PlotWidget()
        self.reconstruction_plot = pg.PlotWidget()
        self.difference_plot = pg.PlotWidget()

        self.original_pen = pg.mkPen(color='b', width=2)
        self.reconstruction_pen = pg.mkPen(color='g', width=2)
        self.difference_pen = pg.mkPen(color='r', width=2, style=QtCore.Qt.DashLine)

        # Set titles and labels
        self.signal_plot.setTitle("Signal Plot")
        self.signal_plot.setLabel("bottom", "Time", units="s")
        self.signal_plot.setLabel("left", "Amplitude")

        self.reconstruction_plot.setTitle("Reconstruction Plot")
        self.reconstruction_plot.setLabel("bottom", "Time", units="s")
        self.reconstruction_plot.setLabel("left", "Amplitude")

        self.difference_plot.setTitle("Difference Plot")
        self.difference_plot.setLabel("bottom", "Time", units="s")
        self.difference_plot.setLabel("left", "Amplitude")
        self.difference_plot.addLegend(offset=(-10, 10))

        # Link the plots for synchronized panning and zooming
        self.reconstruction_plot.setXLink(self.signal_plot)
        self.reconstruction_plot.setYLink(self.signal_plot)
        self.difference_plot.setXLink(self.signal_plot)

    def draw_signal(self, linspace, data_points):
        """Draws a continuous signal in the signal plot."""
        self.signal_plot.clear()
        self.signal_plot.plot(linspace, data_points, pen=self.original_pen, name='Signal')

    def draw_samples(self, linspace, sampled_data):
        """Draws samples as 'x' markers in the signal plot."""
        self.signal_plot.plot(linspace, sampled_data, pen=None, symbol='x', symbolSize=10, symbolBrush='r', name='Samples')

    def draw_reconstruction(self, linspace, reconstruction_data):
        """Draws the reconstructed signal in the reconstruction plot."""
        self.reconstruction_plot.clear()
        self.reconstruction_plot.plot(linspace, reconstruction_data, pen=self.reconstruction_pen, name='Reconstructed Signal')

    def draw_difference(self, linspace, signal_data1, signal_data2):
        """Draws the difference between two signals in the difference plot."""
        if len(signal_data1) != len(signal_data2):
            print("Error: Signal lengths do not match.")
            return
        difference = signal_data1 - signal_data2
        self.difference_plot.clear()
        self.difference_plot.plot(linspace, signal_data1, pen=self.original_pen, name='Original Signal')
        self.difference_plot.plot(linspace, signal_data2, pen=self.reconstruction_pen, name='Reconstructed Signal')
        self.difference_plot.plot(linspace, difference, pen=self.difference_pen, name='Difference')
