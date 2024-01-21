#!/usr/bin/env python

import time
import subprocess as sp
from threading import Thread
from functools import partial
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout


class ClickableLabel(QLabel):
    clicked = Signal()
    hoverin = Signal()
    hoverout= Signal()
    def __init__(self, *args, **kwargs):
        super().__init__()

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        self.clicked.emit()

    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.hoverin.emit()

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self.hoverout.emit()

        
class BaseWidget(QWidget):
    clicked = Signal()
    hoverin = Signal()
    hoverout = Signal()
    def __init__(self, parent=None, polltime=None, listenercmd=None):
        "docstring"
        super(BaseWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.polltime = polltime
        self.listener_output = ""
        if listenercmd:
            self.listener_thread = Thread(target=self.listener_updater, args=[listenercmd])
            self.listener_thread.start()
        if polltime:
            self.poll_thread = Thread(target=self.poll_updater)
            self.poll_thread.start()

    def poll_updater(self):
        while True:
            self.update()
            time.sleep(self.polltime)

    def listener_updater(self, cmd):
        P = sp.Popen(cmd, shell=True, stdout=sp.PIPE, text=True)
        while True:
            self.update()
            self.listener_output = P.stdout.readline().rstrip()

    def update(self):
        'Reimplement to change content on events'
        print('updating')

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        self.clicked.emit()

    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.hoverin.emit()

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self.hoverout.emit()

        
class HerbsluftwmWorkspaces(BaseWidget):
    def __init__(self):
        self.initialised = False
        super().__init__(listenercmd="herbstclient --idle 'tag_changed|tag_flags'")
        self.tags_icons = {
            'WEB': '\uf0ac', 'DEV': '\uf5fc', 'TERM': '\uf120', 'DOCS': '\uf02d',
            'GIMP': '\uf1fc', 'READ': '\uf518', 'AGENDA': '\uf274',
            'DOWN': '\uf019', 'CHAT': '\uf086', 'GAME': '\uf11b'}

        self.format_dict = {':': None, '-': 'orange', '.': 'cyan',
                            '!': 'red', '#': 'white'}

        self.setStyleSheet('padding:2px; margin: 0px; background-color: none; min-width: 25px; font-family: "Font Awesome 6 Free"; font-weight: Bold')

        self.hover_style = "ClickableLabel:hover {background-color: rgba(255, 255, 255, 20%)}"
        self.initUI()

    def initUI(self):
        tags = [tag[1:] for tag in sp.getoutput('herbstclient tag_status').strip().split()]
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        for i, tag in enumerate(tags):
            btn = ClickableLabel()
            btn.setText(self.tags_icons[tag])
            self.hbox.addWidget(btn)
            btn.tag_index = i
            btn.clicked.connect(partial(self.switch_tag, i))
        self.setLayout(self.hbox)
        self.initialised = True
        self.update()

    def switch_tag(self, idx):
        sp.Popen(f'herbstclient use_index {idx}', shell=True)
        
    def update(self):
        if not self.initialised:
            return
        tag_status = sp.getoutput('herbstclient tag_status').strip().split()
        for i, tag in enumerate(tag_status):
            print(tag)
            btn = self.hbox.itemAt(i).widget()
            clr = self.format_dict[tag[0]]
            q_clr = QColor(clr)
            darker_clr = q_clr.darker()
            print(darker_clr.getRgb())
            if tag[0] == ':':
                btn.setStyleSheet('background-color: black')
                continue
            # new_style = f"background-color: {clr}; color: black"
            new_style = f"border-top: 2px solid {clr}"
            print(clr)
            print(new_style)
            btn.setStyleSheet(new_style)
