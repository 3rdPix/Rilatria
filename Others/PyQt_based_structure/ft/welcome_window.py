from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from ft.board import Board
from ft.fun import hpad_this
from ft.styles import dialog_style, title_style_2
import paths as pt


class WelcomeWin(QWidget):

    sg_play = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()
        self.init_gui()
        self.connect_events()

    def init_gui(self) -> None:
        nam1_txt: QLabel = QLabel('Player 1')
        nam2_txt: QLabel = QLabel('Player 2')
        init_stats_txt: QLabel = QLabel('Starting stats')

        self.nam1: QLineEdit = QLineEdit('p1')
        self.nam2: QLineEdit = QLineEdit('p2')
        self.hp: QLineEdit = QLineEdit('6')
        self.vp: QLineEdit = QLineEdit('2')
        self.lp: QLineEdit = QLineEdit('2')
        self.cp: QLineEdit = QLineEdit('2')

        self.play_bt: QPushButton = QPushButton('Play')

        lay = hpad_this(
            (nam1_txt, self.nam1),
            (nam2_txt, self.nam2),
            (init_stats_txt, self.hp, self.vp, self.lp, self.cp),
            self.play_bt
        )

        self.setLayout(lay)

    def connect_events(self) -> None:
        self.play_bt.clicked.connect(self.send_game)

    def send_game(self) -> None:
        info: tuple = (self.nam1.text(), self.nam2.text(), self.hp.text(),
                       self.vp.text(), self.lp.text(), self.cp.text())
        self.sg_play.emit(info)
        self.hide()