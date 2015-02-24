from PySide.QtCore import *
from PySide.QtGui import *
import main_pomodoro
import sys


class Pomodoro(QWidget, main_pomodoro.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.normal_value = 25 * 60 * 60  # 25 mins in ms

    def time_to_ms(self):
        pass

    def apply_options(self):
        pass

    def toggle_timer(self):
        pass

    def update_timer_label(self):
        pass
        # each time signal is emitted for currently active timer

    def next_transition(self):
        pass
        # transition and keep track of normal -> break -> ...


class TimeElapsedThread(QThread):
    """
    Thread for continuous time tracking.
    Emits a secElapsed signal after each second.
    """

    secElapsed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_time_to_zero()
        self.exit = False  # for safe exiting  -  not stuck in while loop

    def run(self):
        timer = QElapsedTimer()
        timer.start()

        while not self.exit:
            if timer.hasExpired(1000):  # 1 seconds expired
                self.secs_elapsed += 1  # secs_elapsed instead of secs because secs is recalculated
                self.set_time_elapsed()  # don't calculate from ms because we always restart the timer
                self.secElapsed.emit()
                timer.restart()

    def set_time_elapsed(self):
        """
        Calculate elapsed hours, minutes, seconds.
        """
        # divmod = divide and modulo -- divmod(1200 / 1000)  =  (1, 200)
        # [0] = division, [1] = remainder(modulo)
        self.mins, self.secs = divmod(self.secs_elapsed, 60)  # s to min
        self.hours, self.mins = divmod(self.mins, 60)  # min to h

    def set_time_to_zero(self):
        self.secs_elapsed, self.secs, self.mins, self.hours = 0, 0, 0, 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
