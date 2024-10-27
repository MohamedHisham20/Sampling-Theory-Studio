import numpy as np


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
        self.linspace_stop = 2
        self.linspace = np.linspace(self.linspace_start, self.linspace_stop, 10_000)
        self.SNR = Signal.MAXIMUM_SNR
        self.maximum_frequency = 0

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
    def add_frequency_component(self, component: SignalComponent):
        if component.frequency > self.maximum_frequency:
            self.maximum_frequency = component.frequency
        self.frequency_components.append(component)

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
        return max([component.frequency for component in self.frequency_components], default=0)

    def get_samples(self, sampling_frequency, with_noise=True):
        sampling_period = 1 / sampling_frequency
        sampling_linspace = np.arange(0, 2, sampling_period)

        return np.interp(sampling_linspace, self.linspace, self.data_points)
