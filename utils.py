import os.path

import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


DATA_FOLDER = "data"
SAMPLING_FREQUENCY = 44100


def get_filepath(filename):
    return os.path.join(DATA_FOLDER, filename)


def load(filename):
    filepath = get_filepath(filename)
    return librosa.load(filepath)


def specshow(C):
    fig, ax = plt.subplots()
    img = librosa.display.specshow(librosa.amplitude_to_db(C, ref=np.max),
                                   sr=SAMPLING_FREQUENCY, x_axis='time', y_axis='cqt_note', ax=ax)
    ax.set_title('Constant-Q power spectrum')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.show()


def waveshow(y):
    _, ax = plt.subplots()
    librosa.display.waveshow(y, sr=SAMPLING_FREQUENCY, ax=ax)
    plt.show()


def constant_q_transform(signal):
    return np.abs(librosa.cqt(signal, sr=SAMPLING_FREQUENCY))


def save_wav(signal, filename):
    filepath = get_filepath(filename)
    wavfile.write(filepath, SAMPLING_FREQUENCY, signal)
