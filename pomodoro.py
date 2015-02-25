from PySide.QtCore import *
from PySide.QtGui import *
import main_pomodoro
import sys


class Pomodoro(QWidget, main_pomodoro.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.time_options = TimeOptions()
        self.timer = TimerThread()

        self.norm_time = self.normTimeEdit.time()
        self.short_time = self.shortTimeEdit.time()
        self.long_time = self.longTimeEdit.time()

        self.timerNormLabel.setText(self.norm_time.toString())
        self.timerShortLabel.setText(self.short_time.toString())
        self.timerLongLabel.setText(self.long_time.toString())

        self.timerButton.clicked.connect(self.toggle_timer)
        self.tabWidget.currentChanged.connect(self.on_options_tab)
        self.timer.secElapsed.connect(self.update_timer_label)

    def on_options_tab(self):
        if self.tabWidget.currentIndex() == 3:  # hide the button on options tab
            self.timerButton.hide()
            return True
        else:
            self.timerButton.show()
            return False

    def apply_options(self):
        self.norm_time = self.normTimeEdit.time()  # -> QTime
        self.short_time = self.shortTimeEdit.time()
        self.long_time = self.longTimeEdit.time()

    def toggle_timer(self):
        self.apply_options()

        if self.tabWidget.currentIndex() == 0:  # 1st tab starts at 0th index
            self.timer.secs_to_run = self.time_options.time_to_secs(self.norm_time)
        elif self.tabWidget.currentIndex() == 1:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.short_time)
        else:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.long_time)

        if self.timer.is_running:
            self.timerButton.setText("Start")
            self.timerButton.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.timer.is_running = False
            self.timer.quit()
        else:
            self.timerButton.setText("Stop")
            self.timerButton.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.timer.is_running = True
            self.timer.start()

    def update_timer_label(self):
        pass
        # each time signal is emitted for currently active timer

    def next_transition(self):
        pass
        # transition and keep track of normal -> break -> ...


class TimeOptions:
    def __init__(self):
        self.set_time_to_zero()

    def set_time_elapsed(self):
        """
        Calculate elapsed hours, minutes, seconds.
        """
        # divmod = divide and modulo -- divmod(1200 / 1000)  =  (1, 200)
        # [0] = division, [1] = remainder(modulo)
        self.mins, self.secs = divmod(self.secs_to_run, 60)  # s to min
        self.hours, self.mins = divmod(self.mins, 60)  # min to h

    def set_time_to_zero(self):
        self.secs_to_run, self.secs, self.mins, self.hours = 25 * 60, 0, 0, 0

    def time_to_secs(self, time):
        return (time.hour() * 60 * 60) + (time.minute() * 60) + (time.second())


class TimerThread(QThread):
    """
    Thread for time tracking.
    Emits a secElapsed signal each second.
    """

    secElapsed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.secs_to_run = 25 * 60  # 25 mins to secs - default
        self.is_running = False

    def run(self):
        timer = QElapsedTimer()
        timer.start()

        while self.secs_to_run > 0 and self.is_running:
            if timer.hasExpired(1000):  # 1 seconds expired
                self.secs_to_run -= 1
                self.secElapsed.emit()
                timer.restart()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
