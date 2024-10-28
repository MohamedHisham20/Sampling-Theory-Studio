import numpy as np
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QListWidget, QSlider, QLineEdit, QListWidgetItem, QCheckBox, QComboBox, QDoubleSpinBox,
                               QGridLayout)
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

        loader = QUiLoader()
        file = QFile("UI/grid_view.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        self.setCentralWidget(self.ui)
        self.ui.showMaximized()
        self.ui.setWindowTitle("Sampling Theory Studio")

        # layout = QVBoxLayout(central_widget)  # Set layout for the central widget
        # controls_layout = QHBoxLayout()

        # Frequency Slider
        self.freq_slider = self.ui.findChild(QSlider, "compose_freq_slider")
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(80)
        self.freq_slider.setValue(30)
        # controls_layout.addWidget(QLabel("Frequency:"))
        # controls_layout.addWidget(self.freq_slider)

        # Phase slider
        self.phase_slider = self.ui.findChild(QSlider, "compose_phase_slider")
        # self.phase_slider.setMinimum(0)
        # self.phase_slider.setMaximum(360)
        # self.phase_slider.setValue(0)
        # controls_layout.addWidget(QLabel("Phase:"))
        # controls_layout.addWidget(self.phase_slider)

        # Amplitude input
        self.amplitude_input = self.ui.findChild(QDoubleSpinBox, "compose_amplitude_spin_box")
        self.amplitude_input.setValue(1.0)
        # controls_layout.addWidget(QLabel("Amplitude:"))
        # controls_layout.addWidget(self.amplitude_input)

        # SNR slider
        self.snr_slider = self.ui.findChild(QSlider, "snr_slider")
        self.snr_slider.setValue(Signal.MAXIMUM_SNR)

        # self.snr_slider.setMinimum(1)
        # self.snr_slider.setMaximum
        # controls_layout.addWidget(QLabel("SNR:"))
        # controls_layout.addWidget(self.snr_slider)

        # Noise checkbox
        self.noise_checkbox = self.ui.findChild(QCheckBox, "show_noise_checkBox")
        self.noise_checkbox.setChecked(True)
        # controls_layout.addWidget(self.noise_checkbox)

        # Checkbox to show samples
        self.show_samples_checkbox = self.ui.findChild(QCheckBox, "show_samples_checkBox")
        self.show_samples_checkbox.setChecked(True)
        # controls_layout.addWidget(self.show_samples_checkbox)

        # Sampling frequency slider
        self.sampling_freq_combobox = self.ui.findChild(QComboBox, "sampling_freq_comboBox")
        self.sampling_freq_combobox.addItem("0.25", 0.25)
        self.sampling_freq_combobox.addItem("0.5", 0.5)
        self.sampling_freq_combobox.addItem("1", 1)
        self.sampling_freq_combobox.addItem("2", 2)
        self.sampling_freq_combobox.addItem("5", 5)
        self.sampling_freq_combobox.addItem("10", 10)
        self.sampling_freq_combobox.setCurrentIndex(3)
        # self.sampling_freq_slider = QSlider(QtCore.Qt.Horizontal)
        # self.sampling_freq_slider.setMinimum(1)
        # self.sampling_freq_slider.setMaximum(10)
        # self.sampling_freq_slider.setValue(2)
        # controls_layout.addWidget(QLabel("Sampling Freq (x Max Freq):"))
        # controls_layout.addWidget(self.sampling_freq_slider)

        # Combo box for reconstruction techniques
        self.reconstruction_method_combobox = self.ui.findChild(QComboBox, "reconstruction_method_comboBox")
        self.reconstruction_method_combobox.addItem("Zero Order Hold", SignalReconstruction.ZERO_ORDER_HOLD)
        self.reconstruction_method_combobox.addItem("Linear", SignalReconstruction.LINEAR)
        self.reconstruction_method_combobox.addItem("Sinc Interpolation", SignalReconstruction.NYQUIST)
        self.reconstruction_method_combobox.addItem("Cubic Spline", SignalReconstruction.CUBIC_SPLINE)
        self.reconstruction_method_combobox.addItem("Fourier", SignalReconstruction.FOURIER)
        self.reconstruction_method_combobox.addItem("Nearest Neighbor", SignalReconstruction.NEAREST_NEIGHBOR)
        self.reconstruction_method_combobox.setCurrentIndex(2)
        # controls_layout.addWidget(QLabel("Reconstruction Technique:"))
        # controls_layout.addWidget(self.reconstruction_method_combobox)

        # Button to add component
        self.add_button = self.ui.findChild(QPushButton, "add_component_button")
        # controls_layout.addWidget(self.add_button)

        # List to display components
        self.components_list = self.ui.findChild(QListWidget, "components_listWidget")
        # layout.addLayout(controls_layout)
        # layout.addWidget(self.components_list)

        # Initialize TimeDomainGraph containing the three linked plots
        self.time_domain_graphs = TimeDomainGraphs()

        self.DFTGraph = DFTGraph()

        self.ui.findChild(QWidget, "top_left_widget").layout().addWidget(self.time_domain_graphs.signal_plot)
        self.ui.findChild(QWidget, "top_right_widget").layout().addWidget(self.time_domain_graphs.reconstruction_plot)
        self.ui.findChild(QWidget, "bottom_left_widget").layout().addWidget(self.time_domain_graphs.difference_plot)
        self.ui.findChild(QWidget, "bottom_right_widget").layout().addWidget(self.DFTGraph.DFT_plot_widget)
        # layout.addLayout(graph_layout)

        top_right_label = self.ui.findChild(QLabel, "top_right_label")
        top_left_label = self.ui.findChild(QLabel, "top_left_label")
        bottom_left_label = self.ui.findChild(QLabel, "bottom_left_label")
        bottom_right_label = self.ui.findChild(QLabel, "bottom_right_label")

        if top_right_label:
            top_right_label.setParent(None)
        if top_left_label:
            top_left_label.setParent(None)
        if bottom_left_label:
            bottom_left_label.setParent(None)
        if bottom_right_label:
            bottom_right_label.setParent(None)

        self.list_view_button = self.ui.findChild(QPushButton, "list_view_button")
        self.grid_view_button = self.ui.findChild(QPushButton, "grid_view_button")
        self.list_view_button.setIcon(QIcon("UI/list_view.png"))
        self.grid_view_button.setIcon(QIcon("UI/grid_view.png"))

        self.ay_7aga = self.ui.findChild(QWidget, "ay_7aga")

        # Connect signals and slots
        self.add_button.clicked.connect(self.add_component)
        self.freq_slider.valueChanged.connect(self.update_active_component)
        self.phase_slider.valueChanged.connect(self.update_active_component)
        self.amplitude_input.textChanged.connect(self.update_active_component)
        self.snr_slider.valueChanged.connect(self.update_snr)
        self.noise_checkbox.stateChanged.connect(self.plot_signal)
        self.sampling_freq_combobox.currentIndexChanged.connect(self.plot_signal)
        self.reconstruction_method_combobox.currentIndexChanged.connect(self.plot_signal)
        self.components_list.itemDoubleClicked.connect(self.remove_component)
        self.list_view_button.clicked.connect(self.show_list_view)
        self.grid_view_button.clicked.connect(self.show_grid_view)

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
        self.amplitude_input.setValue(0)
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
        self.signal.SNR = self.get_snr()
        self.plot_signal()

    def plot_signal(self):
        with_noise = self.noise_checkbox.isChecked()
        data_points = self.signal.get_data_points(with_noise=with_noise)

        # Plot the original signal
        self.time_domain_graphs.draw_signal(self.signal.linspace, data_points)

        # Plot sampled data points if needed
        sampled_data, sample_linspace = self.signal.get_samples(self.sampling_freq_combobox.currentData(), with_noise)
        if self.show_samples_checkbox.isChecked():
            self.time_domain_graphs.draw_samples(sample_linspace, sampled_data)

        # Retrieve selected reconstruction technique
        selected_technique = self.reconstruction_method_combobox.currentData()

        # Perform reconstruction with the selected technique
        maximum_frequency = self.signal.get_maximum_frequency()
        sampling_frequency = self.sampling_freq_combobox.currentData() * maximum_frequency
        reconstruction_obj = SignalReconstruction(sampled_data, sampling_frequency, self.signal.linspace)
        reconstruction_data = reconstruction_obj.reconstruct_signal(selected_technique)

        # Plot the reconstructed signal
        self.time_domain_graphs.draw_reconstruction(self.signal.linspace, reconstruction_data)

        # Difference plot
        self.time_domain_graphs.draw_difference(self.signal.linspace, data_points, reconstruction_data)
        
        #DFT Magnitude Plot
        og_sampling_frequency = 1 / (self.signal.linspace[1]-self.signal.linspace[0])
        self.DFTGraph.draw_DFT_magnitude(data_pnts=data_points, sampling_frequency=og_sampling_frequency)

    def get_snr(self):
        value = self.snr_slider.value()
        if value <= 10:
            return value
        value = value - 9
        return 10 ** value

    def show_list_view(self):
        self.list_view_button.setEnabled(False)
        self.grid_view_button.setEnabled(True)

        original_layout = self.ay_7aga.layout()
        self.ay_7aga.clearLayout(original_layout)

        list_layout = QVBoxLayout()

        list_layout.addWidget(self.time_domain_graphs.signal_plot)
        list_layout.addWidget(self.time_domain_graphs.reconstruction_plot)
        list_layout.addWidget(self.time_domain_graphs.difference_plot)
        list_layout.addWidget(self.DFTGraph.DFT_plot_widget)

        self.ay_7aga.addLayout(list_layout)

    def show_grid_view(self):
        self.list_view_button.setEnabled(True)
        self.grid_view_button.setEnabled(False)

        original_layout = self.ay_7aga.layout()
        self.ay_7aga.clearLayout(original_layout)

        grid_layout = QGridLayout()

        grid_layout.addWidget(self.time_domain_graphs.signal_plot, 0, 0)
        grid_layout.addWidget(self.time_domain_graphs.reconstruction_plot, 0, 1)
        grid_layout.addWidget(self.time_domain_graphs.difference_plot, 1, 0)
        grid_layout.addWidget(self.DFTGraph.DFT_plot_widget, 1, 1)

        self.ay_7aga.addLayout(grid_layout)


    def clear_layout(self, layout):
        # Helper method to clear any existing widgets in the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)



if __name__ == "__main__":
    app = QApplication([])
    window = SamplingStudio()
    app.exec()
