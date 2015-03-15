import ctypes
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import main_pomodoro


class Pomodoro(QWidget, main_pomodoro.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.time_options = TimeOptions()
        self.timer = TimerThread()

        self.active_label = None, None  # (label, "name")
        self.pomodoros = 0

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("Icons/tomato.png"))
        self.tray_icon.activated.connect(self.restore_tray)
        self.tray_icon.messageClicked.connect(self.restore_tray)

        self.apply_options()

        self.soundBox.currentIndexChanged.connect(self.play_select_sound)
        self.tabWidget.currentChanged.connect(self.hide_button_on_options_tab)
        self.tabWidget.currentChanged.connect(self.apply_options)
        self.timerButton.clicked.connect(self.toggle_timerButton)

        self.timer.secElapsed.connect(self.update_active_label)
        self.timer.timerFinished.connect(self.play_select_sound)
        self.timer.timerFinished.connect(self.timer_finished_notification)
        self.timer.timerFinished.connect(self.next_transition)

    def hide_button_on_options_tab(self):
        if self.tabWidget.currentIndex() == 3:  # hide the button on options tab
            self.timerButton.hide()
        else:
            self.timerButton.show()

    def apply_options(self):
        """ Update all labels except the active one with times from the options tab.
        """
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
            self.active_label = (self.timerNormLabel, "Pomodoro")
        elif self.tabWidget.currentIndex() == 1:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.short_time)
            self.active_label = (self.timerShortLabel, "Short")
        else:
            self.timer.secs_to_run = self.time_options.time_to_secs(self.long_time)
            self.active_label = (self.timerLongLabel, "Long")

    def toggle_timerButton(self):
        self.secs_to_run_and_active_label()
        self.apply_options()

        if self.timer.is_running:  # now it's stopped
            self.timerButton.setText("Start")
            self.timerButton.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.timer.is_running = False
            self.timer.delayed_start = (False, 0)
            self.timer.quit()
            self.pomodoros = 0
        else:  # now it's started
            self.timerButton.setText("Stop")
            self.timerButton.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.timer.is_running = True
            if self.transitionCheckBox.isChecked(): self.next_transition(with_button=True)
            else: self.timer.start()

    def update_active_label(self):
        # each time signal is emitted, update label for currently active timer
        time = self.time_options.secs_to_time(self.timer.secs_to_run)
        self.active_label[0].setText(time.toString())

    def next_transition(self, with_button=False):
        # transition and keep track of normal -> break -> ...
        # if self.pomodoros < 4:  # long brake after 4; we start at 0 so 4 is 0,1,2,3
        # self.pomodoros is incremented only if it just finished a pomodoro
        if self.transitionCheckBox.isChecked():
            if self.pomodoros == 0:
                self.tabWidget.setCurrentIndex(0)
                self.pomodoros += 1
            elif self.active_label[1] == "Pomodoro" and self.pomodoros != 4:
                self.tabWidget.setCurrentIndex(1)
                self.pomodoros += 1
            elif self.active_label[1] == "Short":
                self.tabWidget.setCurrentIndex(0)
            elif self.active_label[1] == "Long":
                self.tabWidget.setCurrentIndex(0)
            else:  # on pomodoro tab and next is long
                self.tabWidget.setCurrentIndex(2)
                self.pomodoros = 0  # reset the loop

            # update labels and secs_to_run for next transition
            self.secs_to_run_and_active_label()
            self.apply_options()

            # set the timer to wait 5 seconds before starting
            # dont delay first time
            delay_time = self.time_options.time_to_secs(self.delayTime.time())
            self.timer.delayed_start = (True, delay_time) if not with_button else (False, 0)
            self.timer.start()

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

    def timer_finished_notification(self):
        if self.windowState() & Qt.WindowMinimized and self.doneMinimizedCheck.isChecked():
            self.tray_icon.showMessage("Done", "{0} timer finished.".format(self.active_label[1]))
        elif self.doneFlashCheck.isChecked():
            QApplication.alert(self)

    def restore_tray(self, reason=None):
        if reason == QSystemTrayIcon.Trigger or reason == None:
            self.show()
            self.setWindowState(Qt.WindowActive)
            self.tray_icon.hide()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized and self.minimizeToTrayCheck.isChecked():
                event.ignore()
                QTimer.singleShot(0, self.hide)  # minimize to tray asap
                self.tray_icon.show()
                self.tray_icon.showMessage("Minimized", "The app is minimized. Click on the icon to maximize.")
            elif not self.minimizeToTrayCheck.isChecked():
                event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.tabWidget.setCurrentIndex(0)
        elif event.key() == Qt.Key_F2:
            self.tabWidget.setCurrentIndex(1)
        elif event.key() == Qt.Key_F3:
            self.tabWidget.setCurrentIndex(2)
        elif event.key() == Qt.Key_F4:
            self.tabWidget.setCurrentIndex(3)
        else:
            event.accept()


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
        self.delayed_start = (False, 0)

    def run(self):
        if self.delayed_start[0] and self.delayed_start[1] > 0: self.sleep(self.delayed_start[1])
        while self.secs_to_run > 0 and self.is_running:
            self.sleep(1)
            if self.is_running: self.secs_to_run -= 1; self.secElapsed.emit()  # when stopped it would run otherwise

        if self.secs_to_run == 0: self.timerFinished.emit()


if __name__ == "__main__":
    myappid = 'Marko.pomodoro.python.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    form = Pomodoro()
    form.show()
    app.exec_()
