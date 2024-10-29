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
        
        
    def draw_DFT_magnitude(self, data_pnts: np.ndarray, og_sampling_frequency: int, reconstruction_sampling_frequency: int, signal_freq_components: List[int]):
        """ plots the discrete fourier transform magnitude using FFT
        """
        
        self.DFT_plot_widget.plotItem.clear()
        FFT = np.fft.fft(data_pnts)
        FFT_magnitude = np.abs(FFT)
        fo = np.fft.fftfreq(len(data_pnts), 1/og_sampling_frequency)
            
        self.DFT_plot_widget.plotItem.plot(fo ,FFT_magnitude)
        
        impulse_magnitude = max(FFT_magnitude)

        sampling_frequency_impulses_linspace = np.concatenate([
            np.arange(reconstruction_sampling_frequency / 2, -640, -reconstruction_sampling_frequency),
            np.arange(-reconstruction_sampling_frequency / 2, 640, reconstruction_sampling_frequency)
        ])

        for x in sampling_frequency_impulses_linspace:
            self.DFT_plot_widget.plotItem.plot([x, x], [0, impulse_magnitude], pen='r')



        #
        # for i in range(len(data_pnts)):
        #     if fo[i]==0: continue
        #
        #     #draw impulses at all multiples of the selected sampling frequency
        #     if int(fo[i]) % reconstruction_sampling_frequency == 0:
        #         self.DFT_plot_widget.plotItem.plot([fo[i], fo[i]], [0, impulse_magnitude], pen='r')
        #
        #
        # # draw impulses for periodicities of signal components
        # for f in signal_freq_components:
        #     n  = 1
        #     while pos_aliased_freq <= 640 and neg_aliased_freq >= -640:
        #         pos_aliased_freq = (f + reconstruction_sampling_frequency) * n
        #         neg_aliased_freq = (f - reconstruction_sampling_frequency) * n
        #         self.DFT_plot_widget.plotItem.plot([pos_aliased_freq,pos_aliased_freq], [0, impulse_magnitude], pen="r")        
        #         self.DFT_plot_widget.plotItem.plot([neg_aliased_freq,neg_aliased_freq], [0, impulse_magnitude], pen="r")
        #         n+=1    
        
                
                
        #         self.DFT_plot_widget.plotItem.plot([pos_aliased_freq,pos_aliased_freq], [0, impulse_magnitude], pen="r")
        #         self.DFT_plot_widget.plotItem.plot([neg_aliased_freq,neg_aliased_freq], [0, impulse_magnitude], pen="r")
        #         n+=1
        #
        #
        #
                