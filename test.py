from googletrans import Translator
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy, QGridLayout, QPushButton, QMainWindow
from PyQt5.uic import loadUi
import speech_recognition as sr
import googletrans
import pickle


class inventionGui(QMainWindow):

    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    languageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    emotions = ['Normal', 'Sad', 'Angry', 'Happy']
    colors = ['background-color: cyan',
              'background-color: grey', 'background-color: red', 'background-color: green']

    def __init__(self):
        super(inventionGui, self).__init__()
        loadUi('test.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)

    def fillComboBoxes(self):
        for i in range(len(self.languages)):
            self.comboBox.addItem(str(self.languages[i]))
        for i in range(len(self.emotions)):
            self.emotionBox.addItem(self.emotions[i])

    def record(self):
        self.setStyleSheet(self.colors[self.emotionBox.currentIndex()])
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(
                    audio, language=self.languageCodes[self.comboBox.currentIndex()])
                self.textEdit.setText(said)

            except:
                self.textEdit.setText(self.record())
        return said


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = inventionGui()
    widget.show()
    sys.exit(app.exec_())
