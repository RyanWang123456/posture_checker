# import wave
# from piper import PiperVoice
# import sounddevice as sd

# if __name__ == "__main__":
#     voice = PiperVoice.load("zh_CN-xiao_ya-medium.onnx")

#     with open("input.txt", "r", encoding="utf-8") as f:
#         text = f.read()

#     res = voice.synthesize(text)
#     for chunk in res:
#         sd.play(chunk.audio_float_array, samplerate=chunk.sample_rate)
#         sd.wait()

import os
from kittentts import KittenTTS
import sounddevice as sd
# 1. 指向包含 espeak-ng.exe 的目录
espeak_folder = r"C:\Program Files\eSpeak NG"
os.environ["PATH"] = espeak_folder + os.pathsep + os.environ.get("PATH", "")

# 2. 指向数据目录（非常关键，否则会报错找不到语言包）
os.environ["ESPEAK_DATA_PATH"] = os.path.join(espeak_folder, "espeak-ng-data")

# 3. 如果使用的是 phonemizer 库，有时还需指定库文件路径
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = os.path.join(espeak_folder, "libespeak-ng.dll")


m = KittenTTS("./kitten_tts_nano_v0_2.onnx")
audio = m.generate("good morning")
sd.play(audio, samplerate=24000)
sd.wait()