"""
assistant_core.py - No wake word. Uses WebRTC VAD to detect speech.
Speak anytime; Assistant auto-starts recording and responds.

Handles three kinds of input:
  1. "open <browser> and search for <query>" -> opens browser, speaks answer
  2. "open <app/youtube/google/file explorer>" -> opens it
  3. Anything else -> sent to the LLM as a question

Say "stop" to shut down.
"""
import os
import queue
import tempfile
import wave
import time
import threading

import numpy as np
import sounddevice as sd
import webrtcvad
import pyttsx3

from stt_service import transcribe
from state_machine import StateMachine, State
from llm_service import get_response
from command_router import route
import commands

SAMPLE_RATE = 16000
VAD_FRAME_MS = 30
VAD_FRAME_SAMPLES = int(SAMPLE_RATE * VAD_FRAME_MS / 1000)  # 480
SILENCE_SEC = 1.0
MAX_RECORD_SEC = 10

shutdown_event = threading.Event()


def speak(text: str):
    """
    Fresh pyttsx3 engine per call — reusing one global engine across
    repeated say()/runAndWait() calls is what caused the assistant to
    hang permanently after speaking (known SAPI5 driver bug on Windows).
    """
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine


def safe_get_response(text: str) -> str:
    """Wraps the LLM call so a Groq failure doesn't kill the whole assistant."""
    try:
        return get_response(text)
    except Exception as e:
        print(f"[LLM error] {e}")
        return "Sorry boss, I couldn't reach the AI right now. Try again in a moment."


def handle_command(text: str) -> str | None:
    """
    Routes text through command_router. Returns a response string to speak,
    or None if it was the exit command (caller should shut down).
    """
    data = route(text)
    intent = data["intent"]

    if intent == "empty":
        return None

    if intent == "exit":
        return "exit"

    if intent == "get_time":
        return f"The current time is {commands.get_time()}, boss."

    if intent == "get_date":
        return f"Today's date is {commands.get_date()}, boss."

    if intent == "open_search":
        query = data["query"]
        browser = data["browser"]
        opened = commands.search_web(query, browser)
        if not opened:
            return "Sorry boss, I couldn't open the browser."
        answer = safe_get_response(query)
        return f"Here it is boss. {answer}"

    if intent == "youtube_search":
        query = data["query"]
        opened = commands.youtube_search(query)
        if not opened:
            return "Sorry boss, I couldn't open YouTube."
        return f"Searching YouTube for {query}, boss."

    if intent == "spotify_play":
        query = data["query"]
        ok = commands.spotify_play(query)
        if ok:
            return f"Playing {query} on Spotify, boss."
        return f"Sorry boss, I couldn't play {query} on Spotify — check the Spotify credentials or that the app is installed."

    if intent == "whatsapp_send":
        contact = data["contact"]
        message = data["message"]
        ok, reason = commands.whatsapp_send(contact, message)
        if ok:
            return f"Sent your WhatsApp message to {contact}, boss."
        return reason or "Sorry boss, I couldn't send that WhatsApp message."

    if intent == "open_app":
        target = data["target"]
        if "youtube" in target:
            commands.open_youtube()
            return "Opening YouTube, boss."
        if "google" in target:
            commands.open_google()
            return "Opening Google, boss."
        if "explorer" in target:
            commands.open_app("file explorer")
            return "Opening File Explorer, boss."
        for browser in commands.BROWSER_EXECUTABLES:
            if browser in target:
                commands.open_app(browser)
                return f"Opening {browser.title()}, boss."
        # Generic app: let commands.open_app try Windows App Paths
        # resolution before giving up and falling back to a web search.
        if commands.open_app(target):
            return f"Opening {target.title()}, boss."
        commands.search_web(target)
        return f"I wasn't sure what app that was, so I searched for {target}, boss."

    # intent == "qa"
    return safe_get_response(data["text"])


def main():
    vad = webrtcvad.Vad(3)
    input_dev = 1
    print(f"Using device {input_dev}: {sd.query_devices()[input_dev]['name']}")
    print("\nAssistant listening... (speak anytime, say 'stop' to exit)")

    q = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        q.put(indata.copy().tobytes())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        device=input_dev,
        channels=1,
        dtype="int16",
        blocksize=VAD_FRAME_SAMPLES,
        callback=audio_callback,
    )
    stream.start()

    sm = StateMachine()
    sm.transition(State.IDLE)

    recorded_bytes = bytearray()
    speech_active = False
    silence_frames = 0
    record_start_time = 0.0

    try:
        while not shutdown_event.is_set():
            try:
                pcm_bytes = q.get(timeout=0.1)
            except queue.Empty:
                continue

            is_speech = vad.is_speech(pcm_bytes, SAMPLE_RATE)

            if is_speech:
                if not speech_active:
                    print("\n(Speech detected - recording...)")
                    recorded_bytes.clear()
                    speech_active = True
                    silence_frames = 0
                    record_start_time = time.time()
                recorded_bytes.extend(pcm_bytes)
                silence_frames = 0

                # Enforce max recording length so one long utterance
                # can't block the assistant indefinitely.
                if time.time() - record_start_time > MAX_RECORD_SEC:
                    print("Max recording length hit. Processing...")
                    speech_active = False
                else:
                    continue
            else:
                if speech_active:
                    recorded_bytes.extend(pcm_bytes)
                    silence_frames += 1
                    if silence_frames < int(SILENCE_SEC * 1000 / VAD_FRAME_MS):
                        continue
                    speech_active = False
                else:
                    continue

            print("Processing...")
            audio_np = np.frombuffer(recorded_bytes, dtype=np.int16).copy()

            if np.abs(audio_np).mean() < 150:  # tune this threshold to your mic
                print("(low signal, likely noise - skipping)")
                sm.transition(State.IDLE)
                continue

            wav_path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    wav_path = tmp.name
                    with wave.open(wav_path, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(SAMPLE_RATE)
                        wf.writeframes(audio_np.tobytes())

                print("Transcribing...")
                t0 = time.time()
                text = transcribe(wav_path)
                dt = time.time() - t0
                print(f"You said: {text}  ({dt:.2f}s)")
            except Exception as e:
                print(f"[STT error] {e}")
                sm.transition(State.IDLE)
                if wav_path and os.path.isfile(wav_path):
                    os.unlink(wav_path)
                continue
            finally:
                if wav_path and os.path.isfile(wav_path):
                    os.unlink(wav_path)

            if text.strip() == "":
                print("(empty transcript, ignoring)")
                sm.transition(State.IDLE)
                continue

            sm.transition(State.THINKING)
            response = handle_command(text)

            if response == "exit":
                speak("Goodbye, boss!")
                shutdown_event.set()
                break

            if response is None:
                sm.transition(State.IDLE)
                continue

            sm.transition(State.SPEAKING)
            speak(response)
            # Flush audio captured while the assistant was talking —
            # otherwise it can pick up its own TTS output through the mic
            # and immediately re-trigger on the next loop iteration.
            with q.mutex:
                q.queue.clear()
            sm.transition(State.IDLE)
            print("Listening again...\n")

    except KeyboardInterrupt:
        print("\nShutting down...")
        shutdown_event.set()
    finally:
        stream.stop()
        stream.close()
        print("Cleanup complete.")


if __name__ == "__main__":
    main()
