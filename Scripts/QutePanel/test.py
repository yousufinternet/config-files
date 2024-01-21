#!/usr/bin/env python

import sys
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout



app = QApplication(sys.argv)

wdgt = QWidget()
box = QHBoxLayout()
wdgt.setLayout(box)
lbl = QLabel('🌈🌍🌕🌦🌰 \uf0ac \uf5fc \uf120 \uf02d \uf274 \uf518 \uf1fc')
# fa_font = QFont("Noto Color Emoji", 16)
# app.setFont(fa_font)
lbl.setStyleSheet('font-family: "Font Awesome 6 Free"; font-size: 16pt;font-weight: bold')
box.addWidget(lbl)
wdgt.show()

sys.exit(app.exec_())
