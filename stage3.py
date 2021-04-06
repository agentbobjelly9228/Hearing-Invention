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
        loadUi('form.ui', self)
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
