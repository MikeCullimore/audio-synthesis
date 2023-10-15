# audio-synthesis

Making realistic piano and guitar sounds is hard. Let's play with some simple models and see whether we can make them "good enough".

## Setup

Create a virtual environment:
```bash
python -m venv .venv
```

Activate it (on Unix-like OS):
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Useful links

* [Physical Audio Signal Processing (Stanford)](https://ccrma.stanford.edu/~jos/pasp/)
    * [Piano string wave equation](https://ccrma.stanford.edu/~jos/pasp/Piano_String_Wave_Equation.html)
* [librosa](https://librosa.org/doc/latest/index.html): music and audio analysis.
* [MIT lab on time-frequency analysis](http://web.mit.edu/6.02/www/s2007/lab2.pdf) including simple parametric models of piano strings and composition script.
* [Another implementation of Karplus-Strong](https://github.com/MikeCullimore/guitar-technique/blob/master/generate_audio.py) with more notes in my guitar-technqiue repo.

## TODO

* Additive synthesis.
* Exponential decay envelope.
* ADSR envelope?
* Optimisation ideas:
    * Measure of how close tone is to target audio clip.
    * Define parameter space.
    * Generate random samples in that parameter space.
    * How to define direction, whether change is closer to desired tone or not?
* Combine notes into chords and chords into songs, like [this YouTube video](https://youtu.be/InGrKBRRCUc?si=WH9fd7h9b3mImx1y).
* Function to get frequency given note (MIDI note number?). Librosa?
* Capture inharmonicity:
    * Railsback curve / octave stretching.
    * Harmonics are not integer multiple of fundamental.
* For pianos, capture that there can be multiple strings to a key and they will have slightly different tunings.
* Package up for use in other projects.
* Link with [guitar effects project](https://github.com/MikeCullimore/guitar-effects) to add e.g. distortion.
* FFT
* Wavelets?
* Linter, formatter.
* Select samples from music on file (acoustic guitar, electric guitar, bass, piano, organ).
