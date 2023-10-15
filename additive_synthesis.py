from typing import List, NamedTuple

import librosa
import numpy as np

from utils import SAMPLING_FREQUENCY, constant_q_transform, save_wav, specshow, waveshow


DEFAULT_LENGTH = SAMPLING_FREQUENCY


class ToneParameters(NamedTuple):
    amplitude: float
    frequency: float
    phase: float
    length: int


def tone(parameters: ToneParameters):
    return parameters.amplitude * librosa.tone(
        frequency=parameters.frequency,
        sr=SAMPLING_FREQUENCY,
        length=parameters.length,
        phi=parameters.phase,
    )


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
    
    # TODO: function to generate this for given fundamental and harmonics.
    # TODO: function to combine those into chords.
    parameters_list = [
        ToneParameters(1., 440, 0, DEFAULT_LENGTH),
        ToneParameters(1., 2*440, 0, DEFAULT_LENGTH),
        ToneParameters(1., 3*440, 0, DEFAULT_LENGTH)
    ]
    signal = additive_synthesis(parameters_list, DEFAULT_LENGTH)
    filename = "harmonics example.wav"

    waveshow(signal)

    C = constant_q_transform(signal)
    specshow(C)

    save_wav(signal, filename)


if __name__ == "__main__":
    main()