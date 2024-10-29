import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from SignalClasses import Signal, SignalComponent
from typing import List, Tuple
import numpy as np

class DFTGraph():
    def __init__(self):
        self.DFT_plot_widget = pg.PlotWidget()
        
        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(f)|") #\u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="f", units="HZ")
        self.DFT_plot_widget.plotItem.showGrid(x=True, y=True)
        
        
    def draw_DFT_magnitude(self, data_pnts: np.ndarray, og_sampling_frequency: int, reconstruction_sampling_frequency: int):
        """ plots the discrete fourier transform magnitude using FFT
        """
        self.DFT_plot_widget.plotItem.clear()
        FFT = np.fft.fft(data_pnts)
        FFT_magnitude = np.abs(FFT)
        fo =np.fft.fftfreq(len(data_pnts), 1/og_sampling_frequency)
            
        self.DFT_plot_widget.plotItem.plot(fo ,FFT_magnitude)
        
        for i in range(len(data_pnts)):
            if fo[i]==0: continue
            if int(fo[i]) % reconstruction_sampling_frequency == 0:
                self.DFT_plot_widget.plotItem.plot([fo[i], fo[i]], [0, max(FFT_magnitude)], pen='r')