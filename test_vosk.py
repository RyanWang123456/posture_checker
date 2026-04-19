import json
import threading

import numpy as np
import sounddevice as sd
from vosk import KaldiRecognizer, Model

source_sr = 44100
model = Model("model-en")

def record_until_enter():
    print("recording...")

    frames = []
    stop_event = threading.Event()

    def callback(indata, frame, time_info, status):
        if not stop_event.is_set():
            frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=source_sr,
        channels=1,
        dtype='int16',
        callback=callback
    )

    with stream:
        input()
        stop_event.set()

    if not frames:
        return np.array([], dtype=np.int16)

    audio = np.concatenate(frames, axis=0)
    return audio.flatten()

def transcribe(audio, recognizer):
    recognizer.Reset()

    raw_bytes = audio.tobytes()
    chunk_size = 8000

    for i in range(0, len(raw_bytes), chunk_size):
        recognizer.AcceptWaveform(raw_bytes[i: i + chunk_size])

    result = json.loads(recognizer.FinalResult())
    return result.get("text", "").strip()


if __name__ == "__main__":
    print("loading model...")
    model = Model("model-en")
    rec = KaldiRecognizer(model,source_sr)
    print("successfully loading model...")

    while True:
        input("press enter to start recording...")
        audio = record_until_enter()  
        duration = len(audio) / source_sr
        print(f"finish recording, record time: {duration:.2f}s, start asr...")
        text = transcribe(audio, rec)

        if text:
            print(f"[RESULT]: {text}")
        else:
            print("[RESULT]: EMPTY")
