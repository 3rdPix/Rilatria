from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QComboBox,\
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from ft.fun import hpad_this
import paths as pt
import json


class WelWin(QWidget):

    ant_request_login = pyqtSignal(str)
    ant_update_lang = pyqtSignal(int)

    def __init__(self, lang: int) -> None:
        super().__init__()
        self.set_text(lang)
        self.init_gui()
        self.stylize_gui()
        self.connect_events()

    def set_text(self, lang: int) -> None:
        match lang:
            case 0: file = pt.lang_eng
            case 1: file = pt.lang_spa
            case 2: file = pt.lang_fre
        with open(file, 'r', encoding='utf-8') as raw:
            self.text = json.load(raw).get('login_win')

    def init_gui(self) -> None:
        
        """
        Top
        """
        # frame
        top_frame: QFrame = QFrame()
        top_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)

        # advise text
        self.advise_label: QLabel = QLabel(self.text.get('advise'))
        self.advise_label.setWordWrap(True)

        # language selector
        self.lang_selec: QComboBox = QComboBox()
        english: QIcon = QIcon(pt.pic_english)
        spanish: QIcon = QIcon(pt.pic_spanish)
        french: QIcon = QIcon(pt.pic_french)
        self.lang_selec.addItem(english, 'English')
        self.lang_selec.addItem(spanish, 'Español')
        self.lang_selec.addItem(french, 'Français')

        # layout
        zerogrid1: QGridLayout = QGridLayout()
        zerogrid1.addWidget(self.advise_label, 1, 1, Qt.AlignLeft)
        zerogrid1.addWidget(self.lang_selec, 1, 2, Qt.AlignRight)
        top_frame.setLayout(zerogrid1)

        """
        Bottom
        """
        # frame
        bottom_frame: QFrame = QFrame()
        bottom_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)

        # username text and textbox
        self.username_label: QLabel = QLabel(self.text.get('name'))
        self.username_textbox: QLineEdit = QLineEdit()
        self.play_bt: QPushButton = QPushButton(self.text.get('button'))

        #layout
        bottom_frame.setLayout(hpad_this(
            (self.username_label, self.username_textbox),
            self.play_bt
        ))

        """
        Window Layout
        """
        # internal
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
        self.username_textbox.setFocus()

    def stylize_gui(self) -> None:
        self.setWindowTitle(self.text.get('title'))
        self.setFixedSize(400, 250)
        im_back: QPixmap = QPixmap(pt.pic_welwin_back)
        self.background.setPixmap(im_back)
        self.background.setScaledContents(True)
        with open(pt.qss_welwin, 'r') as css: self.setStyleSheet(css.read())

    def connect_events(self) -> None:
        self.play_bt.clicked.connect(lambda:
            self.ant_request_login.emit(self.username_textbox.text()))
        self.lang_selec.currentIndexChanged.connect(self.redo_text)

    def redo_text(self, lang: int) -> None:
        self.set_text(lang)
        self.advise_label.setText(self.text.get('advise'))
        self.username_label.setText(self.text.get('name'))
        self.play_bt.setText(self.text.get('button'))
        self.setWindowTitle(self.text.get('title'))
        self.ant_update_lang.emit(lang)

    def connection_error_message(self, e: Exception) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(self.text.get('connection_error'))
        msg.setWindowTitle(self.text.get('connection_error_title')) 
        msg.setInformativeText(e.__str__())
        msg.exec_()

    def username_error_message(self, errors: list) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(self.text.get('name_error'))
        msg.setWindowTitle(self.text.get('name_error_title'))
        error = ''
        if 'void' in errors: error = error + self.text.get('name_void')
        if 'len' in errors: error = error + self.text.get('name_len')
        if 'existing' in errors: error = error + self.text.get('name_existing')
        msg.setInformativeText(error) 
        msg.exec_()