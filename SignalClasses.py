import numpy as np
from scipy.ndimage import maximum


class SignalComponent:
    def __init__(self, frequency, amplitude, phase):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.label = f"{amplitude} * sin(2 * pi * {frequency} * t + {phase})"

    def get_data_points(self, linspace):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * linspace + self.phase)


class Signal:
    # Determining signal type
    # --------------------------------------------------------
    COMPOSED = 100
    FROM_FILE = 101

    MAXIMUM_SNR = 100

    # Initializing new objects
    # --------------------------------------------------------
    def __init__(self):
        self.data_points = np.array([])
        self.frequency_components = []
        self.signal_type = Signal.COMPOSED
        self.linspace_start = 0
        self.linspace_stop = 10
        self.linspace = np.linspace(self.linspace_start, self.linspace_stop, 5_000)
        self.SNR = Signal.MAXIMUM_SNR
        self.active_component = SignalComponent(30, 1, 0)

    @staticmethod
    def from_file(file_path):
        new_signal = Signal()
        new_signal.signal_type = Signal.FROM_FILE

        pass

    @staticmethod
    def from_frequency_components(components: [SignalComponent]):
        new_signal = Signal()
        new_signal.signal_type = Signal.COMPOSED
        new_signal.frequency_components = components
        new_signal.maximum_frequency = new_signal.get_maximum_frequency()
        return new_signal

    # Components related methods
    # --------------------------------------------------------
    def update_active_component(self, frequency, amplitude, phase):
        self.active_component.frequency = frequency
        self.active_component.amplitude = amplitude
        self.active_component.phase = phase
        self.active_component.label = f"{amplitude} * sin(2 * pi * {frequency} * t + {phase})"

    def add_frequency_component(self):
        component_copy = SignalComponent(self.active_component.frequency,
                                         self.active_component.amplitude,
                                         self.active_component.phase)
        self.frequency_components.append(component_copy)

        # Reset the active component to default values
        self.active_component = SignalComponent(0, 0, 0)

    def remove_frequency_component(self, removed_component: SignalComponent):
        self.frequency_components.remove(removed_component)
        self.maximum_frequency = self.get_maximum_frequency()

    # --------------------------------------------------------
    def get_data_points(self, with_noise=True):
        # Can change this to return the needed data points type
        if self.signal_type == Signal.COMPOSED:
            data_points = np.sum([
                component.get_data_points(self.linspace) for component in self.frequency_components
            ], axis=0)
            data_points += self.active_component.get_data_points(self.linspace)
        else:
            data_points = self.data_points

        if with_noise:
            # SNR = 10 * log10(P_signal / P_noise)
            signal_power = np.sum(data_points ** 2) / len(data_points)
            noise_power = signal_power / (10 ** (self.SNR / 10))
            noise = np.random.normal(0, np.sqrt(noise_power), len(data_points))
            data_points += noise
        self.data_points = data_points
        return data_points

    def get_maximum_frequency(self):
        if len(self.frequency_components) == 0:
            return self.active_component.frequency
        max_non_zero = max([component.frequency for component in self.frequency_components if component.amplitude != 0],
                           default=0)
        if self.active_component.amplitude != 0:
            return max(max_non_zero, self.active_component.frequency)
        return max_non_zero

    def get_samples(self, sampling_frequency_multiplier, with_noise=True):
        maximum_frequency = self.get_maximum_frequency()
        sampling_frequency = maximum_frequency * sampling_frequency_multiplier
        sampling_period = 1 / sampling_frequency
        sampling_linspace = np.arange(self.linspace_start, self.linspace_stop, sampling_period)

        return np.interp(sampling_linspace, self.linspace, self.data_points), sampling_linspace
