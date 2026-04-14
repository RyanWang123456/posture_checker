import sounddevice as sd
import soundfile as sf

seconds = 5
sample_rate = 16000

audio_data = sd.rec(seconds * sample_rate, samplerate=sample_rate, channels=1)
print("Recording...")
sd.wait()
print("Recording complete.")
sf.write("output.wav", audio_data, sample_rate)
print("Audio saved as output.wav")