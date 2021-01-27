import speech_recognition as sr
import googletrans



class hearingdevice():

    def __init__(self):
        pass

    def getAudio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio, language="en")
            except:
                return getAudio()
        return said

invention = hearingdevice()

while True:
    print(invention.getAudio())
