import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from SignalClasses import Signal, SignalComponent
from typing import List, Tuple
import numpy as np

class DFTGraph(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.DFT_plot_widget = pg.PlotWidget()
        layout.addWidget(self.DFT_plot_widget)
        
        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(\u03C9)|") #\u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="\u03C9", units="rad/s")
        
        
    def draw_DFT_magnitude(self, reconstructed_signal_pnts: np.ndarray):
        """ plots the discrete fourier transform magnitude using FFT
        """
        FFT = np.fft.fft(reconstructed_signal_pnts)
        FFT_magnitude = np.abs(FFT)
            
        self.DFT_plot_widget.plotItem.plot(FFT_magnitude)
        
    def test_plot(self):
        pass    
            
