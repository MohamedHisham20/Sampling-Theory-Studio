import numpy as np
import pandas as pd


class SignalComponent:
    def __init__(self, frequency, amplitude, phase):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.label = f"{amplitude} * cos(2 * pi * {frequency} * t + {phase})"

    def get_data_points(self, linspace):
        return self.amplitude * np.cos(2 * np.pi * self.frequency * linspace + self.phase)

    def to_dict(self):
        return {
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "phase": self.phase
        }


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
        self.linspace_stop = 4
        self.linspace = np.linspace(self.linspace_start, self.linspace_stop, 4000)
        self.data_points = np.zeros_like(self.linspace)
        self.SNR = Signal.MAXIMUM_SNR
        self.active_component = SignalComponent(2, 1, 0)
        self.file_path = None

    def to_dict(self):
        return {
            "components": [component.to_dict() for component in self.frequency_components],
            "active_component": self.active_component.to_dict(),
            "file_path": self.file_path,
            "signal_type": self.signal_type,
            "linspace": self.linspace,
        }

    @staticmethod
    def from_dict(signal_dict):
        if signal_dict["file_path"]:
            new_signal = Signal.from_file(signal_dict["file_path"])
        else:
            new_signal = Signal()
        new_signal.frequency_components = [SignalComponent(**component) for component in signal_dict["components"]]
        new_signal.active_component = SignalComponent(**signal_dict["active_component"])
        new_signal.signal_type = signal_dict["signal_type"]
        new_signal.linspace = signal_dict["linspace"]
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

            new_signal.linspace = data['Time'].values
            new_signal.data_points = data.iloc[:, 1].values  # Use second column as data points
            new_signal.linspace_start = new_signal.linspace[0]
            new_signal.linspace_stop = new_signal.linspace[-1]
            new_signal.active_component = SignalComponent(0, 0, 0)
            new_signal.file_path = file_path

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
        if self.signal_type == Signal.FROM_FILE:
            # interpolate datapoints onto linspace
            data_points = np.interp(linspace, self.linspace, self.data_points)
        else:
            data_points = np.zeros_like(linspace)
        data_points += np.sum([component.get_data_points(linspace) for component in self.frequency_components],
                              axis=0)
        if self.active_component.amplitude != 0:
            data_points += self.active_component.get_data_points(linspace)

        if with_noise:
            # SNR = 10 * log10(P_signal / P_noise)
            signal_power = np.sum(data_points ** 2) / len(data_points)
            noise_power = signal_power / (10 ** (self.SNR / 10))
            noise = np.random.normal(0, np.sqrt(noise_power), len(data_points))
            data_points += noise

        sampling_period = 1 / (sampling_frequency)
        sampling_linspace = np.arange(self.linspace_start, self.linspace_stop, sampling_period)

        sampled_data = np.interp(sampling_linspace, linspace, data_points)

        return data_points, sampled_data, sampling_linspace
