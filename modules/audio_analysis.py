import math
import wave

import numpy as np


def analyze_audio(audio_path):
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
        audio = audio.reshape(-1, channels)
        audio = audio.mean(axis=1)

    duration = len(audio) / sample_rate if sample_rate else 0

    if len(audio) == 0:
        return {
            "duration": 0.0,
            "rms": 0.0,
            "pause_ratio": 0.0,
        }

    audio_float = audio.astype(np.float32)
    rms = float(np.sqrt(np.mean(np.square(audio_float))))

    threshold = max(0.01, rms * 0.5)
    silent = np.abs(audio_float) < threshold
    speaking_samples = np.count_nonzero(~silent)
    speaking_time = speaking_samples / sample_rate if sample_rate else 0
    pause_time = duration - speaking_time
    pause_ratio = pause_time / duration if duration > 0 else 0

    return {
        "duration": round(duration, 2),
        "rms": round(rms, 3),
        "pause_ratio": round(pause_ratio * 100, 2),
    }