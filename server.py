from transformers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def index():
    return {"status": "ok"}

@app.post("/asr")
def asr(audio_data):
    transcript = pipe(audio_data)
    return {"result": transcript["text"]}

