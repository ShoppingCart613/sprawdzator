import random
import string
import sys

from PyQt6.QtWidgets import QDialog, QApplication

from layout import Ui_Dialog


class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.easter.clicked.connect(self.easterClicked)
        self.ui.password.textChanged.connect(self.passwordStrength)

        #zasobnik znakow
        self.smallChars = [l for l in string.ascii_lowercase]
        self.capitalChars = [l for l in string.ascii_uppercase]
        self.numbers = [str(i) for i in range(0,10)]
        self.specialChars = [l for l in string.punctuation]


    def generate(self):
        length = self.ui.passwordLength.text()
        type = self.ui.passwordType.currentText()
        pasword = ''
        if type == 'Pin':
            for i in range(int(length)):
                pasword += str(random.randint(0,9))
        elif self.ui.word.isChecked():
            words = self.readDict('odm.txt')
            while len(pasword) < int(length):
                pasword += random.choice(words)
        else:
            elements = [self.smallChars]
            if self.ui.specialChar.isChecked():
                elements.append(self.specialChars)
            if self.ui.numbers.isChecked():
                elements.append(self.numbers)
            if self.ui.capitalChars.isChecked():
                elements.append(self.capitalChars)

            for i in range(int(length)):
                type = random.randint(0, len(elements)-1)
                pasword += elements[type][random.randint(0, len(elements[type])-1)]

            if self.ui.easter.isChecked() and len(pasword) >= 5:
                max_index = len(pasword) - 6
                start_index = random.randint(0,max_index)
                new_pasword = ''
                easter = 'zając'
                for i in range(len(pasword)):
                    if start_index <= i < start_index+5:
                        new_pasword += easter[i - start_index]
                    else:
                        new_pasword += pasword[i]
                pasword = new_pasword

        self.ui.genertedPassword.setText(pasword)


    def readDict(self, path):
        words = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')[0]
                line = line.replace('\n','')
                if len(line) > 2 and line.find(' ') == -1:
                    words.append(line)
        return words


    def easterClicked(self):
        if self.ui.easter.isChecked():
            self.ui.numbers.setChecked(False)
            self.ui.capitalChars.setChecked(False)
            self.ui.specialChar.setChecked(False)
            self.ui.word.setChecked(False)
            self.ui.numbers.setDisabled(True)
            self.ui.capitalChars.setDisabled(True)
            self.ui.specialChar.setDisabled(True)
            self.ui.word.setDisabled(True)
        else:
            self.ui.numbers.setDisabled(False)
            self.ui.capitalChars.setDisabled(False)
            self.ui.specialChar.setDisabled(False)
            self.ui.word.setDisabled(False)

    def passwordStrength(self):
        pasword = self.ui.password.text()
        str = 0

        for x in pasword:
            if x in self.capitalChars:
                str += 10
            if x in self.numbers:
                str += 15
            if x in self.specialChars:
                str += 20

        if len(pasword) <= 5:
            str -= 30
        if len(pasword) > 5:
            str += int(len(pasword)*4)

        if str > 100:
            str = 100
        if str < 0:
            str = 0

        self.ui.passwordPower.setProperty("value", str)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()

    sys.exit(app.exec())