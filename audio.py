import pyaudio
import wave
import speech_recognition as sr
import os
import keyboard  

def record_audio():
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
    
    print("left ctrl to record right arror to stop")

    keyboard.wait('ctrl')
    print("start record")
    
    frames = []
    recording = True

    def stop_recording(e):
        nonlocal recording
        if e.event_type == keyboard.KEY_DOWN and e.name == 'right':
            recording = False
            print("stop recording")

    keyboard.on_press_key('right', stop_recording)


    while recording:
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
            text = recognizer.recognize_google(audio, language="zh-TW")  
            print(f"you say: {text}")
        except sr.UnknownValueError:
            print("can't defind voice")
        except sr.RequestError as e:
            print(f"voice error{e}")

    os.remove(output)

if __name__ == "__main__":
    record_audio()