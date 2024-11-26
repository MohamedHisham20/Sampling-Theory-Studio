import os.path
import numpy as np
import pandas as pd


class SignalComponent:
    def __init__(self, frequency, amplitude, phase):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.label = f"{amplitude} * cos(2 * pi * {frequency} * t + {phase} * pi)"

    def get_data_points(self, linspace):
        return self.amplitude * np.cos(2 * np.pi * self.frequency * linspace + self.phase * np.pi)

    def to_dict(self):
        return {
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "phase": self.phase
        }


class DataPointsObject:
    def __init__(self):
        self.plot_points = None
        self.noise = None
        self.all_samples = None
        self.plot_samples = None
        self.plot_samples_linspace = None
        self.complete_linspace = None


class Signal:
    # Determining signal type
    # --------------------------------------------------------
    FROM_FILE = 101

    MAXIMUM_SNR = 100

    # Initializing new objects
    # --------------------------------------------------------
    def __init__(self):
        self.frequency_components = []
        self.signal_type = None
        self.linspace_start = 0
        self.linspace_stop = 5
        self.plotting_linspace = np.linspace(self.linspace_start, self.linspace_stop, 10_000)
        self.data_points = np.zeros_like(self.plotting_linspace)
        self.SNR = Signal.MAXIMUM_SNR
        self.active_component = SignalComponent(2, 1, 0)
        self.file_path = None
        self.complete_linspace_start = -10
        self.complete_linspace_stop = 15
        self.complete_linspace_len = (self.complete_linspace_stop - self.complete_linspace_start) * 2_000
        self.sampling_origin_linspace = np.linspace(self.complete_linspace_start,
                                                    self.complete_linspace_stop,
                                                    self.complete_linspace_len)
        self.base_noise = np.random.normal(0, 1, self.complete_linspace_len)

    def to_dict(self):
        return {
            "components": [component.to_dict() for component in self.frequency_components],
            "active_component": self.active_component.to_dict(),
            "file_path": self.file_path,
            "signal_type": self.signal_type,
            "plotting_linspace": {
                "start": self.plotting_linspace[0],
                "stop": self.plotting_linspace[-1],
                "len": len(self.plotting_linspace)
            }
        }

    @staticmethod
    def from_dict(signal_dict):
        if signal_dict["file_path"]:
            complete_path = os.path.join(os.getcwd(), signal_dict["file_path"])
            new_signal = Signal.from_file(complete_path)
        else:
            new_signal = Signal()
        new_signal.frequency_components = [SignalComponent(**component) for component in signal_dict["components"]]
        new_signal.active_component = SignalComponent(**signal_dict["active_component"])
        new_signal.signal_type = signal_dict["signal_type"]
        linspace_start = signal_dict["plotting_linspace"]["start"]
        linspace_stop = signal_dict["plotting_linspace"]["stop"]
        linspace_len = signal_dict["plotting_linspace"]["len"]
        new_signal.plotting_linspace = np.linspace(linspace_start, linspace_stop, linspace_len)
        return new_signal

    @staticmethod
    def from_file(file_path):
        # Read signal data from file
        new_signal = Signal()
        new_signal.signal_type = Signal.FROM_FILE

        # Load data from CSV
        try:
            data = pd.read_csv(file_path)
            if 'Time' not in data.columns or data.columns[1] not in data.columns:
                raise ValueError("CSV file must contain 'Time' and a second column for signal data.")

            new_signal.plotting_linspace = data['Time'].values
            new_signal.data_points = data.iloc[:, 1].values  # Use second column as data points
            new_signal.linspace_start = new_signal.plotting_linspace[0]
            new_signal.linspace_stop = new_signal.plotting_linspace[-1]
            new_signal.active_component = SignalComponent(0, 0, 0)
            path_from_current_working_directory = os.path.relpath(file_path, os.getcwd())
            new_signal.file_path = path_from_current_working_directory

        except Exception as e:
            print(f"Error loading file: {e}")
            return None

        return new_signal

    # Components related methods
    # --------------------------------------------------------
    def update_active_component(self, frequency, amplitude, phase):
        self.active_component.frequency = frequency
        self.active_component.amplitude = amplitude
        self.active_component.phase = phase
        self.active_component.label = f"{amplitude} * sin(2 * pi * {frequency} * t + {phase})"

    def add_frequency_component(self):
        if self.active_component.amplitude == 0 or self.active_component.frequency == 0:
            return
        component_copy = SignalComponent(self.active_component.frequency,
                                         self.active_component.amplitude,
                                         self.active_component.phase)
        self.frequency_components.append(component_copy)

        # Reset the active component to default values
        self.active_component = SignalComponent(0, 0, 0)

    def remove_frequency_component(self, removed_component: SignalComponent):
        self.frequency_components.remove(removed_component)

    # --------------------------------------------------------
    def get_data_points(self, linspace, with_noise=True, sampling_frequency=1):
        # Can change this to return the needed data points type
        return_object = DataPointsObject()
        if self.signal_type == Signal.FROM_FILE:
            data_points = np.interp(linspace, self.plotting_linspace, self.data_points)
            data_points += np.sum([component.get_data_points(linspace) for component in self.frequency_components],
                                  axis=0)
            if self.active_component.amplitude != 0:
                data_points += self.active_component.get_data_points(linspace)
            return_object.plot_points = data_points
        else:
            data_points = np.sum([component.get_data_points(self.sampling_origin_linspace) for component in self.frequency_components],
                                 axis=0)
            if self.active_component.amplitude != 0:
                data_points += self.active_component.get_data_points(self.sampling_origin_linspace)
            return_object.plot_points = np.interp(linspace, self.sampling_origin_linspace, data_points)
            # return_object.plot_points = data_points

        noise = np.zeros_like(data_points)

        if with_noise:
            # SNR = 10 * log10(P_signal / P_noise)
            print("required SNR: ", self.SNR)
            signal_power = np.sum(data_points ** 2) / len(data_points)
            noise_power = signal_power / (10 ** (self.SNR / 10))
            scaling_factor = np.sqrt(noise_power)
            noise = self.base_noise * scaling_factor
            noise_power = np.sum(noise ** 2) / len(noise)
            print("achieved SNR:", 10 * np.log10(signal_power / noise_power))
            # data_points += noise
        return_object.noise = np.interp(linspace, self.sampling_origin_linspace, noise)
        # return_object.noise = noise

        sampling_period = 1 / sampling_frequency
        if self.signal_type == Signal.FROM_FILE:
            all_samples_linspace = np.arange(self.linspace_start, self.linspace_stop, sampling_period)
            points_linspace = linspace
        else:
            all_samples_linspace = np.arange(self.complete_linspace_start, self.complete_linspace_stop, sampling_period)
            points_linspace = self.sampling_origin_linspace
        all_samples = np.interp(all_samples_linspace, points_linspace, data_points + noise)
        return_object.all_samples = all_samples

        sampling_linspace = np.arange(self.linspace_start, self.linspace_stop, sampling_period)
        samples_to_plot = np.interp(sampling_linspace, linspace, return_object.plot_points + return_object.noise)
        return_object.plot_samples = samples_to_plot
        return_object.plot_samples_linspace = sampling_linspace
        # return_object.plot_samples = all_samples
        # return_object.plot_samples_linspace = all_samples_linspace

        return_object.complete_linspace = self.sampling_origin_linspace

        return return_object
