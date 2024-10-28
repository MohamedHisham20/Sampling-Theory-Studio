import pyqtgraph as pg
import numpy as np

class DFTGraph():
    def __init__(self):
        self.DFT_plot_widget = pg.PlotWidget()
        
        self.DFT_plot_widget.plotItem.setTitle("DFT Magnitude Plot")
        self.DFT_plot_widget.plotItem.setLabel(axis="left", text="|F(f)|") #\u03C9
        self.DFT_plot_widget.plotItem.setLabel(axis="bottom", text="f", units="HZ")
        self.DFT_plot_widget.plotItem.showGrid(x=True, y=True)
        
        
    def draw_DFT_magnitude(self, data_pnts: np.ndarray, sampling_frequency: int):
        """ plots the discrete fourier transform magnitude using FFT
        """
        self.DFT_plot_widget.plotItem.clear()
        FFT = np.fft.fft(data_pnts)
        FFT_magnitude = np.abs(FFT)
        fo =np.fft.fftfreq(len(data_pnts), 1/sampling_frequency)
            
        self.DFT_plot_widget.plotItem.plot(fo ,FFT_magnitude)
          
            
