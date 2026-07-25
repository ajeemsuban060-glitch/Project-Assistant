"""
stt_service.py - Speech-to-Text using faster-whisper (CPU, int8).
"""
import os
from faster_whisper import WhisperModel

_model = None
MODEL_SIZE = "base"


def get_model():
    global _model
    if _model is None:
        print(f"Loading faster-whisper '{MODEL_SIZE}' model (int8, CPU)...")
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        print("Model loaded.")
    return _model


def transcribe(audio_file_path: str) -> str:
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    model = get_model()
    # stt_service.py - pin the language so it can't drift to random detection
    segments, info = model.transcribe(audio_file_path, beam_size=5, language="en")
    return " ".join(seg.text.strip() for seg in segments)