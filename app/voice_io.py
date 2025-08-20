import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except sr.RequestError:
            print("❌ Error with the speech recognition service")
            return ""