from googletrans import Translator
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy, QGridLayout, QPushButton, QMainWindow
from PyQt5.uic import loadUi
import speech_recognition as sr
import googletrans


class inventionGui(QMainWindow):

    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    languageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']

    def __init__(self):
        super(inventionGui, self).__init__()
        loadUi('form3.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)

    def fillComboBoxes(self):
        for i in self.languages:
            self.comboBox.addItem(str(i))

    def record(self):
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


class inventionGui(QMainWindow):

    translator = Translator()
    languages = ['English', 'Spanish', 'Cantonese', 'Mandarin', 'French']
    recordLanguageCodes = ['en', 'es', 'zh-yue', 'zh-cmn', 'fr']
    translateLanguageCodes = ['en', 'es', 'zh-TW', 'zh-CN', 'fr']

    def __init__(self):
        super(inventionGui, self).__init__()
        loadUi('form.ui', self)
        self.stocks = ''
        # attaching a function to a buton in your interface
        x = self.fillComboBoxes()
        self.pushButton.clicked.connect(self.record)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = inventionGui()
    widget.show()
    sys.exit(app.exec_())
