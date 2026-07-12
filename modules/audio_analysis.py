import librosa
import numpy as np


def analyze_audio(audio_path):

    # Load Audio
    y, sr = librosa.load(audio_path, sr=None)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)

    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    avg_rms = float(np.mean(rms))

    # Silence Detection
    intervals = librosa.effects.split(
        y,
        top_db=25
    )

    speaking_time = 0

    for start, end in intervals:
        speaking_time += (end - start) / sr

    pause_time = duration - speaking_time

    pause_ratio = pause_time / duration if duration > 0 else 0

    return {
        "duration": round(duration,2),
        "rms": round(avg_rms,3),
        "pause_ratio": round(pause_ratio*100,2)
    }