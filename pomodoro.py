from PySide.QtCore import *
from PySide.QtGui import *
import main_pomodoro
import sys


class Pomodoro(QWidget, main_pomodoro.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
