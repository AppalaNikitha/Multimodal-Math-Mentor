import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment

# Microphone → Text
def listen_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return None

# Audio file (.wav/.mp3) → Text
def audio_file_to_text(file_path):
    recognizer = sr.Recognizer()
    # Convert mp3 → wav if needed
    if file_path.endswith(".mp3"):
        sound = AudioSegment.from_mp3(file_path)
        file_path = "temp.wav"
        sound.export(file_path, format="wav")

    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except:
        return None

# Text → Speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
