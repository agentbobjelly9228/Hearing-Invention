import speech_recognition as sr
import googletrans



class hearingdevice():
    
    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    languageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    def __init__(self):
        for i in range(len(self.languages)):
            print(str(i) + ': ' + self.languages[i])
        self.userLang = int(input("Which language: "))
        self.langCode = self.languageCodes[self.userLang]

    def getAudio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio, language=self.langCode)
            except:
                return self.getAudio()
        return said

invention = hearingdevice()


while True:
    print(invention.getAudio())
