import pyaudio
import wave
import speech_recognition as sr
import os

frames_per_buffer = 3200
format = pyaudio.paInt16
channels = 1
rate = 16000

p = pyaudio.PyAudio()

stream = p.open(
    format=format,
    channels=channels,
    rate=rate,
    input=True,
    frames_per_buffer=frames_per_buffer
)

print("start record")

seconds = 5
frames = []
for i in range(0,int(rate/frames_per_buffer*seconds)):
    data = stream.read(frames_per_buffer)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

output = "open.wav"
obj = wave.open(output,"wb")
obj.setnchannels(channels)
obj.setsampwidth(p.get_sample_size(format))
obj.setframerate(rate)
obj.writeframes(b"".join(frames))
obj.close()

recognizer = sr.Recognizer()

with sr.AudioFile(output) as source:
    audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="zh-TW")  # 轉為繁體中文
        print(f"you say{text}")
    except sr.UnknownValueError:
        print("can't reconize")
    except sr.RequestError as e:
        print(f"voice error{e}")

os.remove(output)