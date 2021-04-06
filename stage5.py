import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy, QGridLayout, QPushButton, QMainWindow
from PyQt5.uic import loadUi
import speech_recognition as sr
from googletrans import Translator
import sounddevice
from scipy.io.wavfile import write


class inventionGui(QDialog):
    def __init__(self):
        super(inventionGui, self).__init__()
        loadUi('form2.ui', self)

        self.pushButton.clicked.connect(self.STT)
        self.pushButton_3.clicked.connect(self.STTTranslator)
        self.exit.clicked.connect(self.exitOut)

    def STT(self):
        self.close()
        widget = STT()
        widget.exec_()

    def STTTranslator(self):
        self.close()
        widget = STTTranslator()
        widget.exec_()

    def exitOut(self):
        exit()


class STT(QDialog):

    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    languageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    fs = 44100
    second = 10
    recordvoice = ''

    def __init__(self):
        super(STT, self).__init__()
        loadUi('form3.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)
        self.back.clicked.connect(self.originalPage)
        self.stop.clicked.connect(self.stopClicked)

    def fillComboBoxes(self):
        for i in self.languages:
            self.comboBox.addItem(str(i))

    def record(self):
        # r = sr.Recognizer()
        # with sr.Microphone() as source:
        #     audio = r.listen(source)
        #     said = ''

        #     try:
        #         said = r.recognize_google(
        #             audio, language=self.languageCodes[self.comboBox.currentIndex()])
        #         self.textEdit.setText(said)

        #     except:
        #         self.textEdit.setText(self.record())
        # return said
        print('recording....')
        self.recordvoice = sounddevice.rec(
            int(self.second * self.fs), samplerate=self.fs, channels=1)

    def originalPage(self):
        self.close()
        widget = inventionGui()
        widget.exec_()

    def stopClicked(self):
        try:
            sounddevice.stop()
            sounddevice.wait()
            print(self.recordvoice)
            print(len(self.recordvoice))
            write('output.wav', self.fs, self.recordvoice)
            print('done')
        except Exception as e:
            print(e)


class STTTranslator(QDialog):

    translator = Translator()
    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    recordLanguageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    translateLanguageCodes = ['en', 'es', 'zh-TW', 'zh-CN', 'fr']

    def __init__(self):
        super(STTTranslator, self).__init__()
        loadUi('form.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)
        self.back.clicked.connect(self.originalPage)

    def fillComboBoxes(self):
        for i in self.languages:
            self.comboBox.addItem(str(i))
            self.comboBox_2.addItem(str(i))

    def record(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(
                    audio, language=self.recordLanguageCodes[self.comboBox.currentIndex()])
                self.textEdit.setText(said)

            except:
                self.textEdit.setText(self.record())
        try:
            print(self.translateLanguageCodes[self.comboBox.currentIndex()])
            print(self.translateLanguageCodes[self.comboBox_2.currentIndex()])
            t = self.translator.translate(
                text=said, src=self.translateLanguageCodes[self.comboBox.currentIndex()], dest=self.translateLanguageCodes[self.comboBox_2.currentIndex()])
            self.textEdit_2.setText(t.text)

        except Exception as e:
            print(e)
        return said

    def originalPage(self):
        self.close()
        widget = inventionGui()
        widget.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = inventionGui()
    widget.show()
    sys.exit(app.exec_())
