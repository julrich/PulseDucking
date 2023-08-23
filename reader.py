import subprocess
import pyaudio
import numpy as np


def monitor(input, supervisor):
    buffer_size = 1024
    pyaudio_format = pyaudio.paInt16
    n_channels = 2
    samplerate = 44100

    zeroCount = 0
    isPlaying = None

    try:
        # TODO: read stderr instead of redirecting to DEVNULL
        proc = subprocess.Popen(
            [
                "parec",
                f"--monitor-stream={str(input.index)}",
                f"--rate={str(samplerate)}",
                f"--channels={str(n_channels)}",
                f"--format={str(pyaudio_format)}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        while True:
            audiobuffer = proc.stdout.read(buffer_size)
            samples = np.fromstring(audiobuffer, dtype=np.int16)
            volume = np.sum(samples**2) / len(samples)

            isZero = volume >= 16384
            newIsPlaying = isPlaying
            if isZero:
                zeroCount += 1
            else:
                zeroCount = 0
                newIsPlaying = True
            if zeroCount > 200:
                newIsPlaying = False

            if newIsPlaying != isPlaying:
                print(f"{input}: {'playing' if newIsPlaying else 'not playing'}")
                isPlaying = newIsPlaying
                supervisor.onPlayStateChange(newIsPlaying)

    except (
        TypeError
    ):  # TypeError: ord() expected a character, but string of length 0 found
        supervisor.onClose(input)
