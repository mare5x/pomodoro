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

        self.apply_options()

        self.active_label = None

        self.timerButton.clicked.connect(self.toggle_timerButton)
        self.tabWidget.currentChanged.connect(self.hide_button_on_options_tab)
        self.timer.secElapsed.connect(self.update_active_label)
        self.timer.timerFinished.connect(self.toggle_timerButton)
        self.timer.timerFinished.connect(self.play_select_sound)

    def hide_button_on_options_tab(self):
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

        self.timerNormLabel.setText(self.norm_time.toString())
        self.timerShortLabel.setText(self.short_time.toString())
        self.timerLongLabel.setText(self.long_time.toString())

    def secs_to_run_and_active_label(self):
        """ Determines secs_to_run and the current active label.
        """
        if self.tabWidget.currentIndex() == 0:  # 1st tab starts at 0th index
            self.timer.secs_to_run = self.time_options.time_to_secs(self.norm_time)
            self.active_label = self.timerNormLabel
        elif self.tabWidget.currentIndex() == 1:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.short_time)
            self.active_label = self.timerShortLabel
        else:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.long_time)
            self.active_label = self.timerLongLabel

    def toggle_timerButton(self):
        self.apply_options()
        self.secs_to_run_and_active_label()

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

    def update_active_label(self):
        # each time signal is emitted, update label for currently active timer
        time = self.time_options.secs_to_time(self.timer.secs_to_run)
        self.active_label.setText(time.toString())

    def next_transition(self):
        pass
        # transition and keep track of normal -> break -> ...

    def play_select_sound(self):
        play_sound = {
            0: QSound.play("Sounds/wristwatch.wav"),
            1: QSound.play("Sounds/doorbell.wav"),
            2: QSound.play("Sounds/alarm.wav"),
            3: QSound.play("Sounds/elevator.wav"),
            4: QSound.play("Sounds/crow.wav"),
            5: None
        }
        # play_sound[self.soundBox.currentIndex()]
        play_sound[0]


class TimeOptions:
    def __init__(self):
        self.set_time_to_zero()

    def secs_to_time(self, secs):
        """
        Calculate elapsed hours, minutes, seconds.
        """
        # divmod = divide and modulo -- divmod(1200 / 1000)  =  (1, 200)
        # [0] = division, [1] = remainder(modulo)
        mins, secs = divmod(secs, 60)  # s to min
        hours, mins = divmod(mins, 60)  # min to h
        return QTime(hours, mins, secs)

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
    timerFinished = Signal()

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

        self.timerFinished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
