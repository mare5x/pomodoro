# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_pomodoro.ui'
#
# Created: Fri Feb 27 19:07:30 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(350, 208)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.normPTab = QtGui.QWidget()
        self.normPTab.setObjectName("normPTab")
        self.gridLayout_2 = QtGui.QGridLayout(self.normPTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.timerNormLabel = QtGui.QLabel(self.normPTab)
        font = QtGui.QFont()
        font.setPointSize(51)
        self.timerNormLabel.setFont(font)
        self.timerNormLabel.setTextFormat(QtCore.Qt.AutoText)
        self.timerNormLabel.setScaledContents(False)
        self.timerNormLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerNormLabel.setIndent(-1)
        self.timerNormLabel.setObjectName("timerNormLabel")
        self.gridLayout_2.addWidget(self.timerNormLabel, 0, 0, 2, 1)
        self.tabWidget.addTab(self.normPTab, "")
        self.shortPTab = QtGui.QWidget()
        self.shortPTab.setObjectName("shortPTab")
        self.gridLayout_3 = QtGui.QGridLayout(self.shortPTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.timerShortLabel = QtGui.QLabel(self.shortPTab)
        font = QtGui.QFont()
        font.setPointSize(51)
        self.timerShortLabel.setFont(font)
        self.timerShortLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerShortLabel.setObjectName("timerShortLabel")
        self.gridLayout_3.addWidget(self.timerShortLabel, 0, 0, 1, 1)
        self.tabWidget.addTab(self.shortPTab, "")
        self.longPTab = QtGui.QWidget()
        self.longPTab.setObjectName("longPTab")
        self.gridLayout_4 = QtGui.QGridLayout(self.longPTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.timerLongLabel = QtGui.QLabel(self.longPTab)
        font = QtGui.QFont()
        font.setPointSize(51)
        self.timerLongLabel.setFont(font)
        self.timerLongLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLongLabel.setObjectName("timerLongLabel")
        self.gridLayout_4.addWidget(self.timerLongLabel, 0, 0, 1, 1)
        self.tabWidget.addTab(self.longPTab, "")
        self.optionsTab = QtGui.QWidget()
        self.optionsTab.setObjectName("optionsTab")
        self.gridLayout_5 = QtGui.QGridLayout(self.optionsTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.longTimeEdit = QtGui.QTimeEdit(self.optionsTab)
        self.longTimeEdit.setTime(QtCore.QTime(0, 10, 0))
        self.longTimeEdit.setObjectName("longTimeEdit")
        self.gridLayout_5.addWidget(self.longTimeEdit, 3, 2, 1, 1)
        self.shortTimeEdit = QtGui.QTimeEdit(self.optionsTab)
        self.shortTimeEdit.setTime(QtCore.QTime(0, 5, 0))
        self.shortTimeEdit.setObjectName("shortTimeEdit")
        self.gridLayout_5.addWidget(self.shortTimeEdit, 2, 2, 1, 1)
        self.label = QtGui.QLabel(self.optionsTab)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.optionsTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 2, 0, 1, 1)
        self.normTimeEdit = QtGui.QTimeEdit(self.optionsTab)
        self.normTimeEdit.setTime(QtCore.QTime(0, 25, 0))
        self.normTimeEdit.setCurrentSection(QtGui.QDateTimeEdit.MinuteSection)
        self.normTimeEdit.setObjectName("normTimeEdit")
        self.gridLayout_5.addWidget(self.normTimeEdit, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.optionsTab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.optionsTab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 4, 0, 1, 1)
        self.soundBox = QtGui.QComboBox(self.optionsTab)
        self.soundBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.soundBox.setFont(font)
        self.soundBox.setObjectName("soundBox")
        self.soundBox.addItem("")
        self.soundBox.addItem("")
        self.soundBox.addItem("")
        self.soundBox.addItem("")
        self.soundBox.addItem("")
        self.soundBox.addItem("")
        self.gridLayout_5.addWidget(self.soundBox, 4, 2, 1, 1)
        self.transitionCheckBox = QtGui.QCheckBox(self.optionsTab)
        self.transitionCheckBox.setChecked(True)
        self.transitionCheckBox.setObjectName("transitionCheckBox")
        self.gridLayout_5.addWidget(self.transitionCheckBox, 5, 1, 1, 2)
        self.tabWidget.addTab(self.optionsTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.timerButton = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.timerButton.setFont(font)
        self.timerButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.timerButton.setObjectName("timerButton")
        self.verticalLayout.addWidget(self.timerButton)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.normTimeEdit, self.shortTimeEdit)
        Form.setTabOrder(self.shortTimeEdit, self.longTimeEdit)
        Form.setTabOrder(self.longTimeEdit, self.soundBox)
        Form.setTabOrder(self.soundBox, self.timerButton)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Simple Pomodoro", None, QtGui.QApplication.UnicodeUTF8))
        self.timerNormLabel.setText(QtGui.QApplication.translate("Form", "25:00", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.normPTab), QtGui.QApplication.translate("Form", "Normal Pomodoro", None, QtGui.QApplication.UnicodeUTF8))
        self.timerShortLabel.setText(QtGui.QApplication.translate("Form", "05:00", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shortPTab), QtGui.QApplication.translate("Form", "Short break", None, QtGui.QApplication.UnicodeUTF8))
        self.timerLongLabel.setText(QtGui.QApplication.translate("Form", "10:00", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.longPTab), QtGui.QApplication.translate("Form", "Long break", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Normal pomodoro: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Short break:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Long break:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Select sound:", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(0, QtGui.QApplication.translate("Form", "Wrist watch Alarm", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(1, QtGui.QApplication.translate("Form", "Door Bell", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(2, QtGui.QApplication.translate("Form", "Alarm Clock", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(3, QtGui.QApplication.translate("Form", "Elevator Ding", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(4, QtGui.QApplication.translate("Form", "Rooster crow", None, QtGui.QApplication.UnicodeUTF8))
        self.soundBox.setItemText(5, QtGui.QApplication.translate("Form", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.transitionCheckBox.setText(QtGui.QApplication.translate("Form", "Auto transition between modes?", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("Form", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.timerButton.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))

