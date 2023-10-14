"""
todo:

Save audio to file (see guitar-technique repo?).
Stretch factors from paper: 2*f/98, i.e. dependent on frequency.
Animate wavetable modification over time.
    Plot single frame.
    Return all wavetables and final waveform.
    Get sample at given time, combine with make_frame(t). Forget efficiency!
Tuning trick in original paper p8 to get closer to desired frequency.
Write up as IPython notebook?
"""


import matplotlib.pyplot as plt
import numpy as np


def plus_minus_ones(num_samples):
    """Generate an array of {-1, 1} chosen at random."""
    return (2*np.random.randint(0, 2, num_samples) - 1).astype(np.float32)


def white_noise(num_samples):
    """Generate array of uniformly-distributed random numbers in the interval [-1, 1]."""
    return np.random.uniform(-1, 1, num_samples).astype(np.float32)


def karplus_strong(frequency, num_samples, stretch_factor=1., sampling_frequency=44100, amplitude=1.):
    # Initialise wavetable.
    # wavetable_size = np.floor(sampling_frequency/frequency).astype(int)
    wavetable_size = np.around(sampling_frequency/frequency).astype(int)
    # wavetable = plus_minus_ones(wavetable_size)
    wavetable = white_noise(wavetable_size)

    # The actual frequency could be slightly off because the wavetable length is an integer.
    # The effect will be more pronounced at high frequencies.
    # Higher sampling frequencies should mitigate the issue?
    # todo: plot error_percent vs frequency.
    # actual_frequency = sampling_frequency/wavetable_size
    # error = actual_frequency - frequency
    # error_percent = 100*error/frequency
    # print(f'Desired frequency: {frequency}')
    # print(f'Actual frequency: {actual_frequency}')
    # print(f'Error: {error}')
    # print(f'Error [%]: {error_percent}')

    signal = np.zeros(num_samples, dtype=np.float32)
    current_sample = 0
    k = 1 - 1/stretch_factor
    for i in range(1, num_samples):
        if np.random.binomial(1, k) == 0:
            wavetable[current_sample] = 0.5*(wavetable[current_sample] + signal[i-1])
        signal[i] = wavetable[current_sample]
        current_sample = (current_sample + 1) % wavetable_size
    
    # Remove DC offset.
    signal -= np.mean(signal)

    signal *= amplitude

    # TODO: return object with metadata (e.g. sampling frequency).
    
    return signal


def plot_signal(signal):
    # TODO: convert time to ms.
    # TODO: plot spectrogram below.
    plt.figure()
    plt.title("Audio waveform")
    plt.plot(signal)
    plt.xlabel("Time [samples]")
    plt.ylabel("Amplitude")
    plt.show()


def main():
    kwargs = {
        # frequency = 27.5  # Lowest note on a piano.
        # frequency = 220
        "frequency": 440,
        # frequency = 4186  # Highest note on a piano. Discrepancy is higher: why?
        "num_samples": 20000,
        "amplitude": 0.5
    }
    signal = karplus_strong(**kwargs)
    plot_signal(signal)


if __name__ == '__main__':
    main()
