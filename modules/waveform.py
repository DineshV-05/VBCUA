import wave

import matplotlib.pyplot as plt
import numpy as np


def plot_waveform(audio_path):
    with wave.open(audio_path, "rb") as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()

    if sample_width == 1:
        dtype = np.uint8
    elif sample_width == 2:
        dtype = np.int16
    elif sample_width == 4:
        dtype = np.int32
    else:
        dtype = np.int16

    audio = np.frombuffer(frames, dtype=dtype)
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)

    times = np.arange(len(audio)) / sample_rate if sample_rate else np.arange(len(audio))

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(times, audio, color="#3b82f6", linewidth=1)
    ax.set_title("Audio Waveform")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()

    return fig