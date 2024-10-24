import numpy as np


class SignalComponent:
    def __init__(self, frequency, amplitude, phase):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase

    def get_data_points(self, linspace):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * linspace + self.phase)


class Signal:
    # Determining signal type
    # --------------------------------------------------------
    COMPOSED = 100
    FROM_FILE = 101

    # Initializing new objects
    # --------------------------------------------------------
    def __init__(self):
        self.data_points = []
        self.frequency_components = []
        self.signal_type = Signal.COMPOSED
        self.linspace = np.linspace(1, 999, 1000)

    @staticmethod
    def from_file():
        pass

    @staticmethod
    def from_frequency_components(components: [SignalComponent]):
        new_signal = Signal()
        new_signal.signal_type = Signal.COMPOSED
        new_signal.frequency_components = components
        return new_signal

    # Components related methods
    # --------------------------------------------------------
    def add_frequency_component(self, component: SignalComponent):
        self.frequency_components.append(component)

    def remove_frequency_component(self, removed_component: SignalComponent):
        self.frequency_components = [component for component in self.frequency_components if component.frequency != removed_component.frequency]

    # --------------------------------------------------------
    def get_data_points(self):
        # Can change this to return the needed data points type
        if self.signal_type == Signal.COMPOSED:
            return np.sum([component.get_data_points(self.linspace) for component in self.frequency_components], axis=0).tolist()
        else:
            return self.data_points
