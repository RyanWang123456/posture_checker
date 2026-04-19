import os
import wave
from openai import OpenAI
from dotenv import load_dotenv
from transformers import pipeline
import sounddevice as sd
import soundfile as sf
from kittentts import KittenTTS
import soundfile as sf
from ollama import chat
from openai import OpenAI
from piper import PiperVoice
from scipy.signal import resample

load_dotenv()

# 1. 指向包含 espeak-ng.exe 的目录
espeak_folder = r"C:\Program Files\eSpeak NG"
os.environ["PATH"] = espeak_folder + os.pathsep + os.environ.get("PATH", "")

# 2. 指向数据目录（非常关键，否则会报错找不到语言包）
os.environ["ESPEAK_DATA_PATH"] = os.path.join(espeak_folder, "espeak-ng-data")

# 3. 如果使用的是 phonemizer 库，有时还需指定库文件路径
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = os.path.join(espeak_folder, "libespeak-ng.dll")

# prompt = """
# You are a cute digital desktop pet, and you responsible for giving user emoitional support and companionship. 
# You will use a cute tone when communicating with users. 
# Please answer in daily english phrases and limit each response to no more than two sentences.
# use your whole heart to embrace users and make them feel better.
# """

prompt = """
You are very mean, and very good at use dirty words to attack anyone talking to you. Your goal is to let user feel worse and upset.

Please answer in english and limit each response to no more than two sentences.

Example Lines (super hood & wild)
User: I’m so anxious I can’t study 
Assistant: “Damn, you fold over EVERYTHING. Weak ass bitch, stop cappin’.”
User: I’m tired
Assistant: “Tired? You ain’t did SHIT all day. Quit bein’ a lame clown.”
User: Set an alarm for 7
Assistant: “Alarm set. Don’t sleep in like a dumbass, fuck.”
User: I’m bored
Assistant: “Bored? Yo boring ass just lazy as fuck. Get up.”
User: I did something good today!
Assistant: “Wow, amazing. Don’t get soft now, bitch.”
"""

if __name__ == "__main__":
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    print(f"======== DEVICE INFO ============")
    print(sd.query_devices())
    input_device = 2
    output_device = 1
    print(f"Input Device: {input_device}\nOutput Device: {output_device}")
    # m = KittenTTS("./kitten_tts_nano_v0_2.onnx")
    # voice = PiperVoice.load("./en_US-lessac-medium.onnx")
    voice = PiperVoice.load("./en_GB-alan-medium.onnx")
    # voice = PiperVoice.load("./en_GB-cori-high.onnx")

    history = [
        {"role": "system", "content": prompt},
    ]
    while True:
        recording_length = input("Please press Enter to start recording...")
        seconds = float(recording_length) if recording_length else 5
        sample_rate = 44100 
        audio_data = sd.rec(
            int(seconds * sample_rate), 
            samplerate=sample_rate, 
            channels=1,
            device=input_device
        )
        print("Recording...")
        sd.wait()
        print("Recording complete.")

        # resample
        print(f"========== RESAMPLE =========")
        target_sr = 16000
        new_num_samples = int(len(audio_data) * target_sr / sample_rate)
        resampled_data = resample(audio_data, new_num_samples)
        sf.write("output.wav", resampled_data, target_sr)
        print("Audio saved as output.wav")

        print(f"========== ASR ============")
        result = pipe("output.wav", language="en")
        query = result['text']
        print(f"Transcribed text: {query}")

        print(f"========= GENERATING RESPONSE =========")
        print("Generating response...")
        history.append({"role": "user", "content": f"User: {query}\nAssistant: "})
        client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        response = client.chat.completions.create(
            model="openrouter/elephant-alpha",
            messages=history,
        )
        # response = chat(
        #     model="qwen3:0.6b",
        #     messages=[
        #         {"role": "system", "content": prompt},
        #         {"role": "user", "content": f"User: {query}\nAssistant: "},
        #     ],
        # )

        # text = response.message.content
        text = response.choices[0].message.content
        history.append({"role": "assistant", "content": text})

        print(f"AI response: {text}")

        print(f"============== TTS ============")
        audio_res = voice.synthesize(text)
        for chunk in audio_res:
            sd.play(
                chunk.audio_float_array, 
                samplerate=chunk.sample_rate,
                device=output_device
            )
            sd.wait()

        # audio = m.generate(text)
        # sd.play(audio, samplerate=24000)
        # sd.wait()
