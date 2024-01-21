#!/usr/bin/env python

import sys
import signal
from widgets import BaseWidget, HerbsluftwmWorkspaces
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QApplication, QFrame, QHBoxLayout, QPushButton, QLabel


class MainPanel(QWidget):
    def __init__(self, x, y, width, height, panel_name="QutePanel"):
        "docstring"
        super().__init__()
        self.x_panel = x
        self.y_panel = y
        self.width_panel = width
        self.height_panel = height
        self.panel_name = panel_name
        self.initUI()

    def frameless(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, on=True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnBottomHint, on=True)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)

    def initUI(self):
        self.frameless()
        self.main_frame = QWidget(self)
        self.main_frame.setProperty("mainframe", "t")
        # self.main_frame.setStyleSheet("*[mainframe=\"t\"]{background-color: rgb(0, 0, 0); border-radius: 12px; padding-left: 5px; padding-right: 10px}")
        hbox=QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.main_frame.setContentsMargins(0, 0, 0, 0)
        self.main_frame.setLayout(self.hbox)
        hbox.addWidget(self.main_frame)
        self.setLayout(hbox)
        self.setWindowTitle(self.panel_name)
        self.setGeometry(self.x_panel, self.y_panel, self.width_panel, self.height_panel)

    def addWidget(self, *args, **kwargs):
        try:
            self.hbox.addWidget(*args, **kwargs)
        except:
            self.hbox.addLayout(*args, **kwargs)

    def insertWidget(self, *args, **kwargs):
        try:
            self.hbox.insertWidget(*args, **kwargs)
        except:
            self.hbox.insertLayout(*args, **kwargs)

    def addStretch(self, *args, **kwargs):
        self.hbox.addStretch(*args, **kwargs)

    def insertStretch(self, *args, **kwargs):
        self.hbox.insertStretch(*args, **kwargs)
        

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet('*{padding: 1px; margin: 0px; color: white; background-color: black; font-family: "Fira Sans Condensed","Font Awesome 6 Free","Font Awesome 6 Brands","Font Awesome","Noto Color Emoji"; font-size: 10pt}')
    panel = MainPanel(100, 0, 1920-200, 25)
    panel.show()
    herbsws = HerbsluftwmWorkspaces()
    herbsws.setParent(panel.main_frame)
    panel.addWidget(herbsws)
    panel.addStretch()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
