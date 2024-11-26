import json
import numpy as np
import pandas as pd
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel,
                               QListWidget, QSlider, QListWidgetItem, QCheckBox, QComboBox, QDoubleSpinBox,
                               QGridLayout, QTabWidget, QFileDialog, QSpinBox)
from PySide6.QtCore import QFile

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

        # Composition sampling frequency
        # self.composition_sampling_freq_slider = self.ui.findChild(QSlider, "compose_sampling_frequency_slider")
        # self.composition_sampling_freq_label = self.ui.findChild(QLabel, "composition_sampling_frequency_label")
        self.plotting_linspace = np.linspace(0, 5, 5_000)

        # Frequency Slider
        self.freq_slider = self.ui.findChild(QSlider, "compose_freq_slider")
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(30)
        self.freq_slider.setValue(2)
        # controls_layout.addWidget(QLabel("Frequency:"))
        # controls_layout.addWidget(self.freq_slider)

        self.frequency_label = self.ui.findChild(QLabel, "compose_hz_label")
        self.frequency_label.setText("2 Hz")

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

        self.show_repetitions_checkbox = self.ui.findChild(QCheckBox, "show_repetitions_checkBox")
        self.show_repetitions_checkbox.setChecked(False)

        # Sampling frequency slider
        self.sampling_freq_spinBox = self.ui.findChild(QSpinBox, "sampling_freq_spinBox")
        self.sampling_freq_spinBox.setMinimum(2)
        self.sampling_freq_spinBox.setMaximum(100)
        self.sampling_freq_spinBox.setValue(6)
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

        self.graphs_container_widget = self.ui.findChild(QWidget, "ay_7aga")
        self.grid_layout = QGridLayout()
        self.show_grid_view()
        self.graphs_container_widget.setLayout(self.grid_layout)

        self.tab_widget = self.ui.findChild(QTabWidget, "tabWidget")
        self.load_signal_button = self.ui.findChild(QPushButton, "browse_csv_button")

        self.export_signal_button = self.ui.findChild(QPushButton, "save_signal_button")

        self.save_scenario_button = self.ui.findChild(QPushButton, "save_scenario_button")

        self.load_scenario_button = self.ui.findChild(QPushButton, "load_scenario_button")

        # Connect signals and slots
        self.add_button.clicked.connect(self.add_component)
        self.freq_slider.valueChanged.connect(self.update_active_component)
        self.phase_slider.valueChanged.connect(self.update_active_component)
        self.amplitude_input.textChanged.connect(self.update_active_component)
        # self.composition_sampling_freq_slider.valueChanged.connect(self.change_composition_sampling_frequency)
        self.snr_slider.valueChanged.connect(self.update_snr)
        self.noise_checkbox.stateChanged.connect(self.plot_signal)
        self.show_samples_checkbox.stateChanged.connect(self.plot_signal)
        self.sampling_freq_spinBox.valueChanged.connect(self.plot_signal)
        self.reconstruction_method_combobox.currentIndexChanged.connect(self.plot_signal)
        self.show_repetitions_checkbox.stateChanged.connect(self.plot_signal)
        self.components_list.itemDoubleClicked.connect(self.remove_component)
        self.list_view_button.clicked.connect(self.show_list_view)
        self.grid_view_button.clicked.connect(self.show_grid_view)
        self.load_signal_button.clicked.connect(self.load_signal)
        self.export_signal_button.clicked.connect(self.export_signal)
        self.save_scenario_button.clicked.connect(self.save_scenario)
        self.load_scenario_button.clicked.connect(self.load_scenario)

        self.show_list_view()

        # Activate noise real-time interference with this
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.plot_signal)
        # self.timer.start()

        self.plot_signal()

    def export_signal(self):
        dataPointsObject = self.signal.get_data_points(self.plotting_linspace, with_noise=False)
        data_points = dataPointsObject.plot_points

        df = pd.DataFrame({'Time': self.plotting_linspace, 'Signal': data_points})

        # Save to CSV
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Signal Data", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)

        df.to_csv(file_path, index=False)

    def load_scenario(self):
        file_path = self.open_file_dialog(type="DSP")
        if file_path is not None:
            self.load_state(file_path)

    def load_state(self, file_path):
        with open(file_path, 'r') as file:
            state_data = json.load(file)

        self.signal = Signal.from_dict(state_data['signal'])
        self.frequency_label.setText(str(self.signal.active_component.frequency) + " Hz")
        self.freq_slider.setValue(self.signal.active_component.frequency)
        self.noise_checkbox.setChecked(state_data['Noise']['show'])
        self.sampling_freq_spinBox.setValue(state_data['sampling']['frequency'])
        self.show_samples_checkbox.setChecked(state_data['sampling']['show'])
        self.show_repetitions_checkbox.setChecked(state_data['sampling']['repeat'])
        self.reconstruction_method_combobox.setCurrentIndex(
            self.reconstruction_method_combobox.findData(state_data['reconstruction_method'])
        )
        self.setSNR(int(state_data['Noise']['SNR']))
        # self.set_composition_sampling_frequency(state_data['composition_sampling_frequency'])
        self.tab_widget.setCurrentIndex(0)
        self.update_component_list()
        self.plot_signal()

    def save_scenario(self):
        # Save the current scenario to a file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Scenario", "", "Scenario Files (*.dsp);;All Files (*)",
                                                   options=options)
        self.save_state(file_path)

    def save_state(self, file_path):
        state_data = {
            'signal': self.signal.to_dict(),
            'Noise': {
                'SNR': self.get_snr(),
                'show': self.noise_checkbox.isChecked()
            },
            'sampling': {
                'frequency': self.sampling_freq_spinBox.value(),
                'show': self.show_samples_checkbox.isChecked(),
                'repeat': self.show_repetitions_checkbox.isChecked()
            },
            'reconstruction_method': self.reconstruction_method_combobox.currentData(),
            # 'composition_sampling_frequency': self.get_compose_sampling_frequency()
        }
        with open(file_path, 'w') as file:
            json.dump(state_data, file)

    def load_signal(self):
        # open a file dialog, and load the signal from the selected file
        file_path = self.open_file_dialog()
        if file_path is not None:
            self.signal = Signal.from_file(file_path)
            self.freq_slider.setValue(1)
            self.phase_slider.setValue(0)
            self.amplitude_input.setValue(0)
            self.frequency_label.setText("1 Hz")
            self.update_component_list()
            if self.signal is not None:
                self.plot_signal()

    def open_file_dialog(self, type="CSV"):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if type == "CSV":
            file_dialog.setNameFilter("CSV files (*.csv)")
        elif type == "DSP":
            file_dialog.setNameFilter("DSP files (*.dsp)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None

    def update_active_component(self):
        frequency = self.freq_slider.value()
        amplitude = float(self.amplitude_input.text())
        phase = self.phase_slider.value() / 8
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
        data_points_object = self.signal.get_data_points(self.plotting_linspace, with_noise,
                                                         self.sampling_freq_spinBox.value())

        data_points = data_points_object.plot_points
        noise = data_points_object.noise
        sampled_data = data_points_object.plot_samples
        sample_linspace = data_points_object.plot_samples_linspace
        all_samples = data_points_object.all_samples
        complete_linspace = data_points_object.complete_linspace

        if data_points is None:
            return

        # Plot the original signal
        self.time_domain_graphs.draw_signal(self.plotting_linspace, data_points + noise)
        # self.time_domain_graphs.draw_signal(complete_linspace, data_points + noise)

        if self.show_samples_checkbox.isChecked():
            self.time_domain_graphs.draw_samples(sample_linspace, sampled_data)

        # Retrieve selected reconstruction technique
        selected_technique = self.reconstruction_method_combobox.currentData()

        # Perform reconstruction with the selected technique
        sampling_frequency = self.sampling_freq_spinBox.value()
        reconstruction_obj = SignalReconstruction(all_samples, sampling_frequency, complete_linspace)
        # returns the data points to be plotted from -7.5s to 12.5s
        reconstruction_data = reconstruction_obj.reconstruct_signal(selected_technique)

        reconstruction_to_plot = np.interp(self.plotting_linspace, complete_linspace, reconstruction_data)

        # Plot the reconstructed signal
        self.time_domain_graphs.draw_reconstruction(self.plotting_linspace, reconstruction_to_plot)
        # self.time_domain_graphs.draw_reconstruction(complete_linspace, reconstruction_data)

        # Difference plot
        self.time_domain_graphs.draw_difference(self.plotting_linspace, data_points, reconstruction_to_plot, self.sampling_freq_spinBox.value(),self.noise_checkbox.isChecked(), self.freq_slider.value())
        # self.time_domain_graphs.draw_difference(complete_linspace, data_points, reconstruction_data)

        # DFT Magnitude Plot
        og_sampling_frequency = self.plotting_linspace[1] - self.plotting_linspace[0]

        show_repetitions = self.show_repetitions_checkbox.isChecked()
        self.DFTGraph.draw_DFT_magnitude(data_points + noise, og_sampling_frequency, sampling_frequency,
                                         show_repetitions)

    def get_snr(self):
        return self.snr_slider.value()

    def setSNR(self, value):
        self.snr_slider.setValue(value)

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
