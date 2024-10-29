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
        self.maximum_frequency = 0

    @staticmethod
    def find_maximum_frequency(data_points, sampling_rate):
        # Compute the FFT of the data points
        fft_result = np.fft.fft(data_points)

        # Calculate the frequency bins corresponding to the FFT result
        freqs = np.fft.fftfreq(len(data_points), d=1 / sampling_rate)

        # Calculate the magnitude spectrum
        magnitude_spectrum = np.abs(fft_result)

        # Consider only positive frequencies and find the maximum
        positive_frequencies = freqs[:len(freqs) // 2]
        positive_magnitude = magnitude_spectrum[:len(magnitude_spectrum) // 2]

        # Find the index of the maximum magnitude
        max_index = np.argmax(positive_magnitude)

        # Get the frequency corresponding to the maximum magnitude
        max_frequency = positive_frequencies[max_index]

        return max_frequency

    @staticmethod
    def from_file(file_path):
        # Read signal data from file
        new_signal = Signal()
        new_signal.signal_type = Signal.FROM_FILE

        # Load data from CSV
        try:
            data = pd.read_csv(file_path)
            # Ensure expected columns are present
            if 'Time' not in data.columns or data.columns[1] not in data.columns:
                raise ValueError("CSV file must contain 'Time' and a second column for signal data.")

            # Assign time and signal data to linspace and data_points
            new_signal.linspace = data['Time'].values
            new_signal.data_points = data.iloc[:, 1].values  # Use second column as data points
            new_signal.linspace_start = new_signal.linspace[0]
            new_signal.linspace_stop = new_signal.linspace[-1]
            new_signal.maximum_frequency = Signal.find_maximum_frequency(new_signal.data_points, 1 / (new_signal.linspace[1] - new_signal.linspace[0]))

        except Exception as e:
            print(f"Error loading file: {e}")
            return None

        return new_signal

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
        if self.signal_type != Signal.COMPOSED:
            return
        self.active_component.frequency = frequency
        self.active_component.amplitude = amplitude
        self.active_component.phase = phase
        self.active_component.label = f"{amplitude} * sin(2 * pi * {frequency} * t + {phase})"

    def add_frequency_component(self):
        if self.active_component.amplitude == 0 or self.active_component.frequency == 0 or self.signal_type != Signal.COMPOSED:
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
    def get_data_points(self, with_noise=True, sampling_frequency_multiplier=2):
        # Can change this to return the needed data points type
        if self.signal_type == Signal.COMPOSED:
            data_points = np.sum([
                component.get_data_points(self.linspace) for component in self.frequency_components
            ], axis=0)
            if self.active_component.amplitude != 0:
                data_points += self.active_component.get_data_points(self.linspace)
        else:
            data_points = self.data_points

        if self.signal_type == self.FROM_FILE and len(data_points) == 0:
            return None, None, None

        if with_noise:
            # SNR = 10 * log10(P_signal / P_noise)
            signal_power = np.sum(data_points ** 2) / len(data_points)
            noise_power = signal_power / (10 ** (self.SNR / 10))
            noise = np.random.normal(0, np.sqrt(noise_power), len(data_points))
            data_points += noise

        sampling_period = 1 / (self.get_maximum_frequency() * sampling_frequency_multiplier)
        sampling_linspace = np.arange(self.linspace_start, self.linspace_stop, sampling_period)

        sampled_data = np.interp(sampling_linspace, self.linspace, data_points)

        return data_points, sampled_data, sampling_linspace

    def get_maximum_frequency(self):
        if self.signal_type == Signal.FROM_FILE:
            return self.maximum_frequency
        if len(self.frequency_components) == 0:
            return self.active_component.frequency
        max_non_zero = max([component.frequency for component in self.frequency_components if component.amplitude != 0],
                           default=0)
        if self.active_component.amplitude != 0:
            return max(max_non_zero, self.active_component.frequency)
        return max_non_zero
