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
    # Data from https://www.jobilize.com/course/section/general-improvements-by-openstax
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


def random_phase():
    # Does randomising the phases of the components improve the sound quality?
    return np.random.uniform(0, 2*np.pi)


def piano_a3_from_fft_plot():
    # http://www-personal.umich.edu/~rbpaul/
    parameters_list = [
        ToneParameters(1.00, 217, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.72, 441, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.38, 658, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.43, 882, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.05, 1102, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.29, 1326, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.10, 1550, random_phase(), DEFAULT_LENGTH),
        ToneParameters(0.02, 1780, random_phase(), DEFAULT_LENGTH)
    ]
    return additive_synthesis(parameters_list)


class ToneParametersWithDecay(NamedTuple):
    amplitude: float
    frequency: float
    decay_rate: float


def tone_with_decay(parameters: ToneParametersWithDecay):
    return parameters.amplitude * librosa.tone(
        frequency=parameters.frequency,
        sr=SAMPLING_FREQUENCY,
        length=DEFAULT_LENGTH,
        phi=random_phase(),
    )


def piano_a3_with_frequency_dependent_decay():
    # TODO: also add some noise? Noise at the start then filter out?
    # TODO: analyse real piano samples to infer relationship between frequency and decay rate.
    # TODO: change units to dB/s?
    # TODO: decouple filtering from harmonics?
    parameters_list = [
        ToneParametersWithDecay(1.00, 217, 0.5),
        ToneParametersWithDecay(0.72, 441, 0.3),
        ToneParametersWithDecay(0.38, 658, 0.2),
        ToneParametersWithDecay(0.43, 882, 0.1),
        ToneParametersWithDecay(0.05, 1102, 0.1),
        ToneParametersWithDecay(0.29, 1326, 0.1),
        ToneParametersWithDecay(0.10, 1550, 0.1),
        ToneParametersWithDecay(0.02, 1780, 0.1)
    ]
    return additive_synthesis_with_decay(parameters_list)


def additive_synthesis(parameters_list: List[ToneParameters]):
    # TODO: is this clipping? Need to normalise all signals to [-1, 1]?
    # TODO: handle inconsistent lengths (pad?).
    signal = np.zeros((DEFAULT_LENGTH,))
    for parameters in parameters_list:
        signal += tone(parameters)
    return signal


def additive_synthesis_with_decay(parameters_list: List[ToneParametersWithDecay]):
    signal = np.zeros((DEFAULT_LENGTH,))
    for parameters in parameters_list:
        decay_parameters = ExponentialDecayParameters(parameters.decay_rate, DEFAULT_LENGTH)
        envelope = exponential_decay(decay_parameters)
        signal += envelope*tone_with_decay(parameters)
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
    # envelope = exponential_decay(ExponentialDecayParameters(0.2, DEFAULT_LENGTH))
    # signal = envelope*additive_synthesis(parameters_list)
    # filename = "exponential decay.wav"
    # signal = envelope*piano_c4_from_fft_plot()
    # signal = envelope*piano_a3_from_fft_plot()
    # filename = "piano A3 from FFT plot (random phases).wav"

    signal = piano_a3_with_frequency_dependent_decay()
    filename = "piano A3 from FFT plot (frequency dependent decay).wav"

    waveshow(signal)

    C = constant_q_transform(signal)
    specshow(C)

    save_wav(signal, filename)


if __name__ == "__main__":
    main()
