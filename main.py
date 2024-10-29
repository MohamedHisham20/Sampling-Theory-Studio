import sys

import numpy as np
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel,
                               QListWidget, QSlider, QListWidgetItem, QCheckBox, QComboBox, QDoubleSpinBox,
                               QGridLayout, QTabWidget, QFileDialog)
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
        self.freq_slider.setMaximum(30)
        self.freq_slider.setValue(1)
        # controls_layout.addWidget(QLabel("Frequency:"))
        # controls_layout.addWidget(self.freq_slider)

        self.frequency_label = self.ui.findChild(QLabel, "compose_hz_label")
        self.frequency_label.setText("1 Hz")

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
        self.sampling_freq_combobox.addItem("0.5", 0.5)
        self.sampling_freq_combobox.addItem("1", 1)
        self.sampling_freq_combobox.addItem("2", 2)
        self.sampling_freq_combobox.addItem("3", 3)
        self.sampling_freq_combobox.addItem("4", 4)
        self.sampling_freq_combobox.setCurrentIndex(2)
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

        # self.ui.findChild(QWidget, "top_left_widget").layout().addWidget(self.time_domain_graphs.signal_plot)
        # self.ui.findChild(QWidget, "top_right_widget").layout().addWidget(self.time_domain_graphs.reconstruction_plot)
        # self.ui.findChild(QWidget, "bottom_left_widget").layout().addWidget(self.time_domain_graphs.difference_plot)
        # self.ui.findChild(QWidget, "bottom_right_widget").layout().addWidget(self.DFTGraph.DFT_plot_widget)
        # layout.addLayout(graph_layout)

        self.list_view_button = self.ui.findChild(QPushButton, "list_view_button")
        self.grid_view_button = self.ui.findChild(QPushButton, "grid_view_button")
        self.list_view_button.setIcon(QIcon("UI/list_view.png"))
        self.grid_view_button.setIcon(QIcon("UI/grid_view.png"))

        self.ay_7aga = self.ui.findChild(QWidget, "ay_7aga")
        self.grid_layout = QGridLayout()
        self.show_grid_view()
        self.ay_7aga.setLayout(self.grid_layout)

        self.tab_widget = self.ui.findChild(QTabWidget, "tabWidget")
        self.load_signal_button = self.ui.findChild(QPushButton, "browse_csv_button")

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
        self.load_signal_button.clicked.connect(self.load_signal)
        self.tab_widget.currentChanged.connect(self.change_signal_type)

        # Timer for real-time updates
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.plot_signal)
        self.timer.start()

    def change_signal_type(self):
        index = self.tab_widget.currentIndex()
        if index == 0:
            self.signal.signal_type = Signal.COMPOSED
        else:
            self.signal.signal_type = Signal.FROM_FILE

    def load_signal(self):
        # open a file dialog, and load the signal from the selected file
        file_path = self.open_file_dialog()
        if file_path is not None:
            self.signal = Signal.from_file(file_path)
            if self.signal is not None:
                self.plot_signal()

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None

    def update_active_component(self):
        frequency = self.freq_slider.value()
        amplitude = float(self.amplitude_input.text())
        phase = np.radians(self.phase_slider.value())
        self.signal.update_active_component(frequency, amplitude, phase)
        self.plot_signal()
        string = str(frequency) + " Hz"
        self.frequency_label.setText(string)

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
        data_points, sampled_data, sample_linspace = self.signal.get_data_points(with_noise, self.sampling_freq_combobox.currentData())
        if data_points is None:
            return

        # Plot the original signal
        self.time_domain_graphs.draw_signal(self.signal.linspace, data_points)

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
        
        self.DFTGraph.draw_DFT_magnitude(data_points, og_sampling_frequency, sampling_frequency, False)

    def get_snr(self):
        value = self.snr_slider.value()
        if value <= 10:
            return value
        value = value - 9
        return 10 ** value

    def show_list_view(self):
        self.list_view_button.setEnabled(False)
        self.grid_view_button.setEnabled(True)

        self.clear_grid_layout()

        self.grid_layout.addWidget(self.time_domain_graphs.signal_plot, 0, 0)
        self.grid_layout.addWidget(self.time_domain_graphs.reconstruction_plot, 1, 0)
        self.grid_layout.addWidget(self.time_domain_graphs.difference_plot, 2, 0)
        self.grid_layout.addWidget(self.DFTGraph.DFT_plot_widget, 3, 0)

    def show_grid_view(self):
        self.list_view_button.setEnabled(True)
        self.grid_view_button.setEnabled(False)

        self.clear_grid_layout()

        self.grid_layout.addWidget(self.time_domain_graphs.signal_plot, 0, 0)
        self.grid_layout.addWidget(self.time_domain_graphs.reconstruction_plot, 0, 1)
        self.grid_layout.addWidget(self.time_domain_graphs.difference_plot, 1, 0)
        self.grid_layout.addWidget(self.DFTGraph.DFT_plot_widget, 1, 1)

    def clear_grid_layout(self):
        self.grid_layout.removeWidget(self.time_domain_graphs.signal_plot)
        self.grid_layout.removeWidget(self.time_domain_graphs.reconstruction_plot)
        self.grid_layout.removeWidget(self.time_domain_graphs.difference_plot)
        self.grid_layout.removeWidget(self.DFTGraph.DFT_plot_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = SamplingStudio()
    app.exec()
