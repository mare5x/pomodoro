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

        self.active_label = None, None  # (label, "name")
        self.pomodoros = 0

        self.apply_options()

        self.soundBox.currentIndexChanged.connect(self.play_select_sound)
        self.tabWidget.currentChanged.connect(self.hide_button_on_options_tab)
        self.tabWidget.currentChanged.connect(self.apply_options)
        self.timerButton.clicked.connect(self.toggle_timerButton)

        self.timer.secElapsed.connect(self.update_active_label)
        self.timer.timerFinished.connect(self.play_select_sound)
        self.timer.timerFinished.connect(self.next_transition)

    def hide_button_on_options_tab(self):
        if self.tabWidget.currentIndex() == 3:  # hide the button on options tab
            self.timerButton.hide()
        else:
            self.timerButton.show()

    def apply_options(self):
        self.norm_time = self.normTimeEdit.time()  # -> QTime
        self.short_time = self.shortTimeEdit.time()
        self.long_time = self.longTimeEdit.time()

        # make a list of tuples of labels to be updated (label, timeEdit)
        inactive_labels = [inactive_label for inactive_label in
                          [(self.timerNormLabel, self.norm_time),
                           (self.timerShortLabel, self.short_time),
                           (self.timerLongLabel, self.long_time)]
                          if inactive_label[0] != self.active_label[0]]

        for label in inactive_labels:
            label[0].setText(label[1].toString())

    def secs_to_run_and_active_label(self):
        """ Determines secs_to_run and the current active label.
        """
        if self.tabWidget.currentIndex() == 0:  # 1st tab starts at 0th index
            self.timer.secs_to_run = self.time_options.time_to_secs(self.norm_time)
            self.active_label = (self.timerNormLabel, "pomodoro")
        elif self.tabWidget.currentIndex() == 1:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.short_time)
            self.active_label = (self.timerShortLabel, "short")
        else:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.long_time)
            self.active_label = (self.timerLongLabel, "long")

    def toggle_timerButton(self):
        self.secs_to_run_and_active_label()
        self.apply_options()

        if self.timer.is_running:  # now it's stopped
            self.timerButton.setText("Start")
            self.timerButton.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.timer.is_running = False
            self.timer.quit()
            self.pomodoros = 0
        else:  # now it's started
            self.timerButton.setText("Stop")
            self.timerButton.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.timer.is_running = True
            if self.transitionCheckBox.isChecked(): self.next_transition()
            else: self.timer.start()

    def update_active_label(self):
        # each time signal is emitted, update label for currently active timer
        time = self.time_options.secs_to_time(self.timer.secs_to_run)
        self.active_label[0].setText(time.toString())

    def next_transition(self):
        # transition and keep track of normal -> break -> ...
        # if self.pomodoros < 4:  # long brake after 4; we start at 0 so 4 is 0,1,2,3
        if self.transitionCheckBox.isChecked():
            if self.pomodoros == 0:
                self.tabWidget.setCurrentIndex(0)
                self.pomodoros += 1
            elif self.active_label[1] == "pomodoro" and self.pomodoros != 4:
                self.tabWidget.setCurrentIndex(1)
                self.pomodoros += 1
            elif self.active_label[1] == "short":
                self.tabWidget.setCurrentIndex(0)
            elif self.active_label[1] == "long":
                self.tabWidget.setCurrentIndex(0)
            else:  # on pomodoro tab and next is long
                self.tabWidget.setCurrentIndex(2)
                self.pomodoros = 0  # reset the loop

            self.secs_to_run_and_active_label()
            self.apply_options()
            self.timer.start()

            print(self.pomodoros)

    def play_select_sound(self):
        sounds = {
            0: "Sounds/wristwatch.wav",
            1: "Sounds/doorbell.wav",
            2: "Sounds/alarm.wav",
            3: "Sounds/elevator.wav",
            4: "Sounds/crow.wav",
            5: None
        }
        QSound.play(sounds[self.soundBox.currentIndex()])


class TimeOptions:

    @staticmethod
    def secs_to_time(secs):
        """
        Calculate elapsed hours, minutes, seconds.
        """
        # divmod = divide and modulo -- divmod(1200 / 1000)  =  (1, 200)
        # [0] = division, [1] = remainder(modulo)
        mins, secs = divmod(secs, 60)  # s to min
        hours, mins = divmod(mins, 60)  # min to h
        return QTime(hours, mins, secs)

    @staticmethod
    def time_to_secs(time):
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

        if self.secs_to_run == 0: self.timerFinished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
