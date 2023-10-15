from typing import List, NamedTuple

import librosa
import numpy as np

from utils import SAMPLING_FREQUENCY, constant_q_transform, save_wav, specshow, waveshow


DEFAULT_LENGTH = SAMPLING_FREQUENCY


# TODO: include sampling frequency here?
class ToneParameters(NamedTuple):
    amplitude: float
    frequency: float
    phase: float
    length: int


class ExponentialDecayParameters(NamedTuple):
    decay_rate: float
    length: int


def tone(parameters: ToneParameters):
    return parameters.amplitude * librosa.tone(
        frequency=parameters.frequency,
        sr=SAMPLING_FREQUENCY,
        length=parameters.length,
        phi=parameters.phase,
    )


def exponential_decay(parameters: ExponentialDecayParameters):
    time = np.arange(parameters.length) / SAMPLING_FREQUENCY
    signal: np.ndarray = np.exp(-time/parameters.decay_rate)
    return signal


def harmonics_array(fundamental: float, num_harmonics: int):
    # TODO: ampltiudes as array?
    parameters_list = []
    for i in range(1, num_harmonics + 1):
        parameters_list.append(ToneParameters(1/i, i*fundamental, 0, DEFAULT_LENGTH))
    return parameters_list


def piano_c4_from_fft_plot():
    # The following parameters are measured from a real piano.
    # Resulting sound is still not particularly good, shows the limits of additive synthesis.
    # https://www.jobilize.com/course/section/general-improvements-by-openstax
    parameters_list = [
        ToneParameters(0.15, 93, 0, DEFAULT_LENGTH),
        ToneParameters(0.07, 175, 0, DEFAULT_LENGTH),
        ToneParameters(1.00, 261, 0, DEFAULT_LENGTH),
        ToneParameters(0.66, 521, 0, DEFAULT_LENGTH),
        ToneParameters(0.12, 782, 0, DEFAULT_LENGTH),
        ToneParameters(0.03, 1043, 0, DEFAULT_LENGTH),
        ToneParameters(0.05, 1304, 0, DEFAULT_LENGTH),
        ToneParameters(0.08, 1571, 0, DEFAULT_LENGTH),
        ToneParameters(0.09, 1839, 0, DEFAULT_LENGTH),
        ToneParameters(0.02, 2117, 0, DEFAULT_LENGTH)
    ]
    return additive_synthesis(parameters_list)


def additive_synthesis(parameters_list: List[ToneParameters]):
    # TODO: handle inconsistent lengths (pad?).
    signal = np.zeros((DEFAULT_LENGTH,))
    for parameters in parameters_list:
        signal += tone(parameters)
    # TODO: normalise amplitude?
    return signal


def main():
    # tone_parameters = ToneParameters(1., 440, 0, DEFAULT_LENGTH)
    # signal = tone(tone_parameters)
    # filename = "tone example.wav"
    
    # TODO: function to generate list of frequencies with inharmonicity (how to quantify?).
    # TODO: function to combine those into chords.
    # TODO: decouple harmonics from envelope, i.e. generate all with amplitude 1 then shape in frequency domain?
    # TODO: frequency-dependent decay rates.
    # parameters_list = harmonics_array(440, 20)
    envelope = exponential_decay(ExponentialDecayParameters(0.5, DEFAULT_LENGTH))
    # signal = envelope*additive_synthesis(parameters_list)
    # filename = "exponential decay.wav"
    signal = envelope*piano_c4_from_fft_plot()
    filename = "piano C4 from FFT plot.wav"

    waveshow(signal)

    C = constant_q_transform(signal)
    specshow(C)

    save_wav(signal, filename)


if __name__ == "__main__":
    main()
