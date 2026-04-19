import sounddevice as sd
import soundfile as sf

seconds = 1
sample_rate = 44100 

input_device = 2
output_device = 1
print(sd.query_devices())

audio_data = sd.rec(
    int(5 * sample_rate), 
    samplerate=sample_rate, 
    channels=1,
    device=input_device
)
print(f"Start Recording...")
sd.wait()
print(f"Finish Recording...")

print(f"Playing Audio...")
sd.play(audio_data, sample_rate, device=output_device)
sd.wait()
print(f"Finish Playing...")
