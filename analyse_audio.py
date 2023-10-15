from utils import constant_q_transform, load, specshow, waveshow


def main():
    filename = "01 Toccata and Fugue for organ in D minor, BWV 565.mp3"
    # TODO: pass sampling_frequency to subsequent functions (can't assume 44kHz!).
    signal, sampling_frequency = load(filename)

    waveshow(signal)

    C = constant_q_transform(signal)
    specshow(C)

    # TODO: plot frequency transform as animation over time.


if __name__ == "__main__":
    main()