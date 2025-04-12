import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Please go ahead... Listening...")

        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Unable to request results from Speech Recognition Server; {e}")

if __name__ == "__main__":
    speech_to_text()
