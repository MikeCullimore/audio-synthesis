"""
todo:

Move unrelated functions to separate file(s).
Stretch factors from paper: 2*f/98, i.e. dependent on frequency.
Animate wavetable modification over time.
    Plot single frame.
    Return all wavetables and final waveform.
    Get sample at given time, combine with make_frame(t). Forget efficiency!
Tuning trick in original paper p8 to get closer to desired frequency.
Write up as IPython notebook?
"""


import os.path

import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


DATA_FOLDER = "data"
SAMPLING_FREQUENCY = 44100


def plus_minus_ones(num_samples):
    """Generate an array of {-1, 1} chosen at random."""
    return (2*np.random.randint(0, 2, num_samples) - 1).astype(np.float32)


def white_noise(num_samples):
    """Generate array of uniformly-distributed random numbers in the interval [-1, 1]."""
    return np.random.uniform(-1, 1, num_samples).astype(np.float32)


def karplus_strong(frequency, smoothing_factor, amplitude=1.):
    if (smoothing_factor < 0) or (smoothing_factor > 1):
        raise ValueError(f'smoothing_factor must be in the range [0, 1].')
    
    num_samples = 2*SAMPLING_FREQUENCY
    
    # Initialise wavetable.
    # wavetable_size = np.floor(SAMPLING_FREQUENCY/frequency).astype(int)
    wavetable_size = np.around(SAMPLING_FREQUENCY/frequency).astype(int)
    # wavetable = plus_minus_ones(wavetable_size)
    wavetable = white_noise(wavetable_size)

    # The actual frequency could be slightly off because the wavetable length is an integer.
    # The effect will be more pronounced at high frequencies.
    # Higher sampling frequencies should mitigate the issue?
    # todo: plot error_percent vs frequency.
    # actual_frequency = SAMPLING_FREQUENCY/wavetable_size
    # error = actual_frequency - frequency
    # error_percent = 100*error/frequency
    # print(f'Desired frequency: {frequency}')
    # print(f'Actual frequency: {actual_frequency}')
    # print(f'Error: {error}')
    # print(f'Error [%]: {error_percent}')

    # Generate signal.
    signal = np.zeros(num_samples, dtype=np.float32)
    current_sample = 0
    previous_value = 0
    a = smoothing_factor
    b = 1 - smoothing_factor
    for i in range(num_samples):
        wavetable[current_sample] = a*wavetable[current_sample] + b*previous_value
        signal[i] = wavetable[current_sample]
        previous_value = signal[i]
        current_sample = (current_sample + 1) % wavetable_size
    
    # Remove DC offset.
    signal -= np.mean(signal)

    signal *= amplitude

    # TODO: return object with metadata (e.g. sampling frequency).
    
    return signal


def constant_q_transform(signal):
    return np.abs(librosa.cqt(signal, sr=SAMPLING_FREQUENCY))


def specshow(C):
    fig, ax = plt.subplots()
    img = librosa.display.specshow(librosa.amplitude_to_db(C, ref=np.max),
                                   sr=SAMPLING_FREQUENCY, x_axis='time', y_axis='cqt_note', ax=ax)
    ax.set_title('Constant-Q power spectrum')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.show()


def waveshow(y):
    # TODO: convert time to ms.
    # TODO: plot spectrogram below.
    # TODO: use librosa waveshow, specshow.
    # plt.figure()
    # plt.title("Audio waveform")
    # plt.plot(signal)
    # plt.xlabel("Time [samples]")
    # plt.ylabel("Amplitude")
    # plt.show()
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=SAMPLING_FREQUENCY, ax=ax)
    plt.show()


def save_wav(signal, filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    wavfile.write(filepath, SAMPLING_FREQUENCY, signal)


def main():
    # TODO: type for this.
    kwargs = {
        # frequency = 27.5  # Lowest note on a piano.
        # frequency = 220
        "frequency": 440,
        # frequency = 4186  # Highest note on a piano. Discrepancy is higher: why?
        "smoothing_factor": 0.5,
        "amplitude": 0.5
    }
    signal = karplus_strong(**kwargs)
    C = constant_q_transform(signal)
    
    waveshow(signal)
    specshow(C)
    
    # filename = "Karplus-Strong example.wav"
    # save_wav(signal, filename)


if __name__ == '__main__':
    main()
