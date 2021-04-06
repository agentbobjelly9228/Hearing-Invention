import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy, QGridLayout, QPushButton, QMainWindow
from PyQt5.uic import loadUi
import speech_recognition as sr
from googletrans import Translator
import sounddevice
from scipy.io.wavfile import write
import wavio
import pickle
import librosa as lr
import numpy as np
import os
import time


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
    fs = 22050
    second = 1000
    recordvoice = ''
    picklein = open('classifier.pickle', 'rb')
    classifier = pickle.load(picklein)
    colors = ['background-color: cyan', 'background-color: yellow',
              'background-color: red']
    emotions = ['None', 'Happy', 'Angry']

    def __init__(self):
        super(STT, self).__init__()
        loadUi('form3.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)
        self.back.clicked.connect(self.originalPage)
        self.stop.clicked.connect(self.stopClicked)
        self.emotionBox.currentIndexChanged.connect(self.changeEmotion)

    def fillComboBoxes(self):
        for i in self.languages:
            self.comboBox.addItem(str(i))
        for i in range(len(self.emotions)):
            self.emotionBox.addItem(self.emotions[i])

    def record(self):
        try:
            sounddevice.default.reset()
            print('recording....')
            self.recordvoice = ''
            self.recordvoice = sounddevice.rec(
                int(self.second * self.fs), samplerate=self.fs, channels=1)
        except Exception as e:
            print(e)

    def originalPage(self):
        self.close()
        widget = inventionGui()
        widget.exec_()

    def stopClicked(self):
        try:

            sounddevice.stop()
            self.recordvoice = self.recordvoice[self.recordvoice != 0]
            print(self.recordvoice)
            sounddevice.get_stream()
            print(len(self.recordvoice))
            write('output.wav', self.fs, np.array([0, 0, 0, 0, 0, 0]))
            write('output.wav', self.fs, self.recordvoice)
            print('done')
            test, fs = lr.load('output.wav')
            sounddevice.play(self.recordvoice, 22050)
            print(fs)
            print(test)
            test = np.array(test)
            test = test[test != 0]
            test = np.mean(lr.feature.mfcc(test, sr=22050).T, axis=0)
            print(test)
            emoIndex = self.classifier.predict([test])[0]
            print(emoIndex)
            wavio.write('output.wav', self.recordvoice, self.fs, sampwidth=2)
            r = sr.Recognizer()
            with sr.AudioFile('output.wav') as source:
                audio = r.listen(source)
                said = ''

                try:
                    said = r.recognize_google(
                        audio, language=self.languageCodes[self.comboBox.currentIndex()])
                    self.textEdit.setText(said)

                except Exception as e:
                    print(e)
            if emoIndex == 0:
                self.emotionBox.setCurrentIndex(2)
                self.setStyleSheet(self.colors[2])
            else:
                self.emotionBox.setCurrentIndex(1)
                self.setStyleSheet(self.colors[1])
        except Exception as e:
            print(e)

    def changeEmotion(self):
        self.setStyleSheet(self.colors[self.emotionBox.currentIndex()])


class STTTranslator(QDialog):

    translator = Translator()
    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    recordLanguageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    translateLanguageCodes = ['en', 'es', 'zh-TW', 'zh-CN', 'fr']
    colors = ['background-color: cyan', 'background-color: yellow',
              'background-color: red']
    emotions = ['None', 'Happy', 'Angry']
    fs = 22050
    second = 1000
    recordvoice = ''
    picklein = open('classifier.pickle', 'rb')
    classifier = pickle.load(picklein)

    def __init__(self):
        super(STTTranslator, self).__init__()
        loadUi('form.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)
        self.back.clicked.connect(self.originalPage)
        self.stop.clicked.connect(self.stopClicked)
        self.emoBox.currentIndexChanged.connect(self.changeEmotion)

    def fillComboBoxes(self):
        for i in self.languages:
            self.comboBox.addItem(str(i))
            self.comboBox_2.addItem(str(i))
        for emotion in self.emotions:
            self.emoBox.addItem(emotion)

    def record(self):
        sounddevice.default.reset()
        print('recording....')
        self.recordvoice = ''
        self.recordvoice = sounddevice.rec(
            int(self.second * self.fs), samplerate=self.fs, channels=1)

    def stopClicked(self):
        try:

            sounddevice.stop()
            self.recordvoice = self.recordvoice[self.recordvoice != 0]
            print(self.recordvoice)
            sounddevice.get_stream()
            print(len(self.recordvoice))
            write('output.wav', self.fs, np.array([0, 0, 0, 0, 0, 0]))
            write('output.wav', self.fs, self.recordvoice)
            print('done')
            test, fs = lr.load('output.wav')
            sounddevice.play(self.recordvoice, 22050)
            print(fs)
            print(test)
            test = np.array(test)
            test = test[test != 0]
            test = np.mean(lr.feature.mfcc(test, sr=22050).T, axis=0)
            print(test)
            emoIndex = self.classifier.predict([test])[0]
            print(emoIndex)
            wavio.write('output.wav', self.recordvoice, self.fs, sampwidth=2)
            r = sr.Recognizer()
            with sr.AudioFile('output.wav') as source:
                audio = r.listen(source)
                said = ''

                try:
                    said = r.recognize_google(
                        audio, language=self.translateLanguageCodes[self.comboBox.currentIndex()])
                    self.textEdit.setText(said)

                except Exception as e:
                    print(e)
            t = self.translator.translate(
                text=said, src=self.translateLanguageCodes[self.comboBox.currentIndex()], dest=self.translateLanguageCodes[self.comboBox_2.currentIndex()])
            self.textEdit_2.setText(t.text)
            if emoIndex == 0:
                self.emoBox.setCurrentIndex(2)
                self.setStyleSheet(self.colors[2])
            else:
                self.emoBox.setCurrentIndex(1)
                self.setStyleSheet(self.colors[1])
        except Exception as e:
            print(e)

    def originalPage(self):
        self.close()
        widget = inventionGui()
        widget.exec_()

    def changeEmotion(self):
        self.setStyleSheet(self.colors[self.emoBox.currentIndex()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = inventionGui()
    widget.show()
    sys.exit(app.exec_())
