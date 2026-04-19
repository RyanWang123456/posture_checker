from datetime import datetime

import numpy as np
import sounddevice as sd
from transformers import pipeline

sample_rate = 44100 

input_device = 2
output_device = 1
print(sd.query_devices())

print("loading model...")
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")
while True:
    seconds = int(input("Seconds to record: ")) 
    # input("press enter to start recording...")
    print(f"Start Recording...")
    audio_data = sd.rec(
        int(seconds * sample_rate), 
        samplerate=sample_rate, 
        channels=1,
        device=input_device
    )
    sd.wait()
    print(f"Finish Recording...")

    print(audio_data.shape)

    # resample
    # print(f"Start Resample...")
    # target_sr = 16000
    # new_num_samples = int(len(audio_data) * target_sr / sample_rate)
    # resampled_data = resample(audio_data, new_num_samples)
    # print(f"Finish Resample...")

    # print(f"Playing Audio...")
    # sd.play(resampled_data, target_sr, device=output_device)
    # sd.wait()
    # print(f"Finish Playing...")


    print(f"Playing Audio...")
    sd.play(audio_data, sample_rate, device=output_device)
    sd.wait()
    print(f"Finish Playing...")

    starttime = datetime.now()
    audio_input = {
        "sampling_rate": 44100,
        "raw": np.ravel(audio_data)
    }
    result = pipe(audio_input) 
    query = result['text']
    endtime = datetime.now()
    print(f"Transcribed text: {query}")
    print(f"Time elapsed: {(endtime - starttime).microseconds / 1000:.2f} seconds")
