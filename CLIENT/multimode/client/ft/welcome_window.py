from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout,\
    QLabel, QPushButton, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from ft.fun import hpad_this
import paths as pt


class WelWin(QWidget):

    sg_play = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.init_gui()
        self.stylize_gui()
        self.connect_events()

    def init_gui(self) -> None:
        
        # Top
        top_frame: QFrame = QFrame()
        top_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
        top_frame.setLineWidth(1)
        with open(pt.txt_advise, 'r') as raw: advise_text = raw.read()
        advise_label: QLabel = QLabel(text=advise_text)
        advise_label.setWordWrap(True)
        zerogrid1: QGridLayout = QGridLayout()
        zerogrid1.addWidget(advise_label)
        top_frame.setLayout(zerogrid1)

        # Bottom
        bottom_frame: QFrame = QFrame()
        bottom_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
        bottom_frame.setLineWidth(1)
        username_label: QLabel = QLabel('Hero name:')
        self.username_textbox: QLineEdit = QLineEdit()
        self.username_textbox.setFocus()
        self.play_bt: QPushButton = QPushButton(text='Enter legend')
        bottom_frame.setLayout(hpad_this(
            (username_label, self.username_textbox),
            self.play_bt
        ))

        # Background and container
        self.background: QLabel = QLabel()
        self.background.setObjectName('backLabel')
        v_lay: QVBoxLayout = QVBoxLayout()
        v_lay.addStretch()
        v_lay.addWidget(top_frame)
        v_lay.addWidget(bottom_frame)
        v_lay.addStretch()
        self.background.setLayout(v_lay)

        # Window
        drawer = QGridLayout()
        drawer.addWidget(self.background)
        drawer.setContentsMargins(0, 0, 0, 0)
        self.setLayout(drawer)

    def stylize_gui(self) -> None:
        self.setFixedSize(370, 200)

        im_back: QPixmap = QPixmap(pt.im_welwin_back)
        self.background.setPixmap(im_back)
        self.background.setScaledContents(True)

        with open(pt.css_welwin, 'r') as css: style = css.read()
        self.setStyleSheet(style)

    def connect_events(self) -> None:
        self.play_bt.clicked.connect(self.send_game)

    def send_game(self) -> None:
        self.sg_play.emit(self.username_textbox.text())
        self.hide()