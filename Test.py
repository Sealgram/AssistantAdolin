import speech_recognition as sr

def recognize():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
        text = r.recognize_google(audio)
    return text

print(recognize())