import numpy as np
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QListWidget, QSlider, QLineEdit, QListWidgetItem, QCheckBox, QComboBox)
from PySide6.QtCore import QFile
from pyqtgraph.Qt import QtCore

from SignalClasses import Signal
from TimeDomainGraphs import TimeDomainGraphs
from SignalReconstruction import SignalReconstruction
from DFTGraph import DFTGraph



class SamplingStudio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.signal = Signal()

        self.setWindowTitle("Sampling Theory Studio")
        self.showMaximized()

        loader = QUiLoader()
        file = QFile("UI/grid_view.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        self.setCentralWidget(self.ui)

        # layout = QVBoxLayout(central_widget)  # Set layout for the central widget
        # controls_layout = QHBoxLayout()

        # Frequency Slider
        # self.freq_slider = QSlider(QtCore.Qt.Horizontal)
        # self.freq_slider.setMinimum(1)
        # self.freq_slider.setMaximum(80)
        # self.freq_slider.setValue(30)
        # controls_layout.addWidget(QLabel("Frequency:"))
        # controls_layout.addWidget(self.freq_slider)

        # Phase slider
        # self.phase_slider = QSlider(QtCore.Qt.Horizontal)
        # self.phase_slider.setMinimum(0)
        # self.phase_slider.setMaximum(360)
        # self.phase_slider.setValue(0)
        # controls_layout.addWidget(QLabel("Phase:"))
        # controls_layout.addWidget(self.phase_slider)

        # Amplitude input
        # self.amplitude_input = QLineEdit()
        # self.amplitude_input.setText("1.0")
        # controls_layout.addWidget(QLabel("Amplitude:"))
        # controls_layout.addWidget(self.amplitude_input)

        # SNR slider
        # self.snr_slider = QSlider(QtCore.Qt.Horizontal)
        # self.snr_slider.setMinimum(1)
        # self.snr_slider.setMaximum(Signal.MAXIMUM_SNR)
        # self.snr_slider.setValue(Signal.MAXIMUM_SNR)
        # controls_layout.addWidget(QLabel("SNR:"))
        # controls_layout.addWidget(self.snr_slider)

        # Noise checkbox
        # self.noise_checkbox = QCheckBox("Show Noise")
        # self.noise_checkbox.setChecked(True)
        # controls_layout.addWidget(self.noise_checkbox)

        # Checkbox to show samples
        # self.show_samples_checkbox = QCheckBox("Show Samples")
        # self.show_samples_checkbox.setChecked(True)
        # controls_layout.addWidget(self.show_samples_checkbox)

        # Sampling frequency slider
        # self.sampling_freq_slider = QSlider(QtCore.Qt.Horizontal)
        # self.sampling_freq_slider.setMinimum(1)
        # self.sampling_freq_slider.setMaximum(10)
        # self.sampling_freq_slider.setValue(2)
        # controls_layout.addWidget(QLabel("Sampling Freq (x Max Freq):"))
        # controls_layout.addWidget(self.sampling_freq_slider)

        # Combo box for reconstruction techniques
        self.reconstruction_method_combobox = self.ui.findChild(QComboBox, "reconstruction_method_combobox")
        self.reconstruction_method_combobox.addItem("Zero Order Hold", SignalReconstruction.ZERO_ORDER_HOLD)
        self.reconstruction_method_combobox.addItem("Linear", SignalReconstruction.LINEAR)
        self.reconstruction_method_combobox.addItem("Nyquist", SignalReconstruction.NYQUIST)
        self.reconstruction_method_combobox.addItem("Cubic Spline", SignalReconstruction.CUBIC_SPLINE)
        self.reconstruction_method_combobox.addItem("Fourier", SignalReconstruction.FOURIER)
        self.reconstruction_method_combobox.addItem("Nearest Neighbor", SignalReconstruction.NEAREST_NEIGHBOR)
        controls_layout.addWidget(QLabel("Reconstruction Technique:"))
        controls_layout.addWidget(self.reconstruction_method_combobox)

        # Button to add component
        self.add_button = QPushButton("Add Component")
        controls_layout.addWidget(self.add_button)

        # List to display components
        self.components_list = QListWidget()
        # layout.addLayout(controls_layout)
        # layout.addWidget(self.components_list)

        # Initialize TimeDomainGraph containing the three linked plots
        self.time_domain_graphs = TimeDomainGraphs()

        self.DFTGraph = DFTGraph()

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.time_domain_graphs.signal_plot)
        graph_layout.addWidget(self.time_domain_graphs.reconstruction_plot)
        graph_layout.addWidget(self.time_domain_graphs.difference_plot)
        graph_layout.addWidget(self.DFTGraph.DFT_plot_widget)

        # layout.addLayout(graph_layout)

        # Connect signals and slots
        self.add_button.clicked.connect(self.add_component)
        self.freq_slider.valueChanged.connect(self.update_active_component)
        self.phase_slider.valueChanged.connect(self.update_active_component)
        self.amplitude_input.textChanged.connect(self.update_active_component)
        self.snr_slider.valueChanged.connect(self.update_snr)
        self.noise_checkbox.stateChanged.connect(self.plot_signal)
        self.sampling_freq_slider.valueChanged.connect(self.plot_signal)
        self.reconstruction_method_combobox.currentIndexChanged.connect(self.plot_signal)
        self.components_list.itemDoubleClicked.connect(self.remove_component)

        # Timer for real-time updates
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.plot_signal)
        self.timer.start()

    def update_active_component(self):
        frequency = self.freq_slider.value()
        amplitude = float(self.amplitude_input.text())
        phase = np.radians(self.phase_slider.value())
        self.signal.update_active_component(frequency, amplitude, phase)

    def add_component(self):
        self.signal.add_frequency_component()
        self.update_component_list()
        self.plot_signal()
        self.amplitude_input.setText("0")
        self.update_active_component()

    def remove_component(self, item):
        index = self.components_list.row(item)
        if index != -1:
            removed_component = self.signal.frequency_components[index]
            self.signal.remove_frequency_component(removed_component)
            self.update_component_list()
            self.plot_signal()

    def update_component_list(self):
        self.components_list.clear()
        for component in self.signal.frequency_components:
            list_item = QListWidgetItem(component.label)
            self.components_list.addItem(list_item)

    def update_snr(self):
        self.signal.SNR = self.snr_slider.value()
        self.plot_signal()

    def plot_signal(self):
        with_noise = self.noise_checkbox.isChecked()
        data_points = self.signal.get_data_points(with_noise=with_noise)

        # Plot the original signal
        self.time_domain_graphs.draw_signal(self.signal.linspace, data_points)

        # Plot sampled data points if needed
        sampled_data, sample_linspace = self.signal.get_samples(self.sampling_freq_slider.value(), with_noise)
        if self.show_samples_checkbox.isChecked():
            self.time_domain_graphs.draw_samples(sample_linspace, sampled_data)

        # Retrieve selected reconstruction technique
        selected_technique = self.reconstruction_method_combobox.currentData()

        # Perform reconstruction with the selected technique
        maximum_frequency = self.signal.get_maximum_frequency()
        sampling_frequency = self.sampling_freq_slider.value() * maximum_frequency
        reconstruction_obj = SignalReconstruction(sampled_data, sampling_frequency, self.signal.linspace)
        reconstruction_data = reconstruction_obj.reconstruct_signal(selected_technique)

        # Plot the reconstructed signal
        self.time_domain_graphs.draw_reconstruction(self.signal.linspace, reconstruction_data)

        # Difference plot
        self.time_domain_graphs.draw_difference(self.signal.linspace, data_points, reconstruction_data)
        
        #DFT Magnitude Plot
        og_sampling_frequency = 1 / (self.signal.linspace[1]-self.signal.linspace[0])
        self.DFTGraph.draw_DFT_magnitude(data_pnts=data_points, sampling_frequency=og_sampling_frequency)


if __name__ == "__main__":
    app = QApplication([])
    window = SamplingStudio()
    app.exec()
