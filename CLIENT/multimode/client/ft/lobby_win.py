from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QComboBox,\
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from ft.fun import hpad_this
import paths as pt
import json



class LobbyWin(QWidget):

    ant_request_login = pyqtSignal(str)
    ant_update_lang = pyqtSignal(int)

    def __init__(self, lang: int) -> None:
        super().__init__()
        self.set_text(lang)
        self.init_gui()
        self.stylize_gui()

    def set_text(self, lang: int) -> None:
        match lang:
            case 0: file = pt.lang_eng
            case 1: file = pt.lang_spa
            case 2: file = pt.lang_fre
        with open(file, 'r', encoding='utf-8') as raw:
            self.text = json.load(raw).get('lobby_win')

    def init_gui(self) -> None:
        
        """
        Top
        """
        # frame
        top_frame: QFrame = QFrame()
        top_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)

        self.lobby_name = QLabel(self.text.get('lobby_name'))
        self.lobby_name.setObjectName('title')
        zerogrid1 = QGridLayout()
        zerogrid1.addWidget(self.lobby_name)
        zerogrid1.setAlignment(Qt.AlignCenter)
        top_frame.setLayout(zerogrid1)

        """
        Middle
        """
        # frame
        middle_frame = QFrame()
        middle_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)

        box_p1 = QLabel()
        box_p1.setObjectName('p_boxes')
        box_p1.setMaximumSize(210, 210)
        im_p1 = QPixmap(pt.pic_p1)
        photo_p1 = QLabel()
        photo_p1.setPixmap(im_p1)
        photo_p1.setScaledContents(True)
        photo_p1.setFixedSize(90, 110)
        self.p_name = QLabel()
        self.p_name.setObjectName('PName')
        minugrid1 = QGridLayout()
        minugrid1.addWidget(photo_p1, 1, 1, Qt.AlignTop)
        minugrid1.addWidget(self.p_name, 2, 1, Qt.AlignCenter)
        box_p1.setLayout(minugrid1)

        box_p2 = QLabel()
        box_p2.setObjectName('p_boxes')
        box_p2.setMaximumSize(210, 210)
        im_p2 = QPixmap(pt.pic_p2)
        photo_p2 = QLabel()
        photo_p2.setPixmap(im_p2)
        photo_p2.setScaledContents(True)
        photo_p2.setFixedSize(90, 110)
        p2_name = QLabel('Searching...')
        p2_name.setObjectName('PName')
        minugrid2 = QGridLayout()
        minugrid2.addWidget(photo_p2, 1, 1, Qt.AlignTop)
        minugrid2.addWidget(p2_name, 2, 1, Qt.AlignCenter)
        box_p2.setLayout(minugrid2)

        zerogrid2 = QGridLayout()
        zerogrid2.addWidget(box_p1, 1, 1)
        zerogrid2.addWidget(box_p2, 1, 2)
        middle_frame.setLayout(zerogrid2)

        """
        Bottom
        """
        # frame
        bottom_frame: QFrame = QFrame()
        bottom_frame.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)

        self.information_text = QLabel(self.text.get('information'))
        self.information_text.setObjectName('info')
        self.information_text.setWordWrap(True)
        zerogrid3 = QHBoxLayout()
        zerogrid3.addStretch(1)
        zerogrid3.addWidget(self.information_text, 3)
        zerogrid3.addStretch(1)
        zerogrid3.setAlignment(Qt.AlignCenter)
        bottom_frame.setLayout(zerogrid3)

        """
        Window Layout
        """
        # internal
        self.background: QLabel = QLabel()
        self.background.setObjectName('backLabel')
        v_lay: QVBoxLayout = QVBoxLayout()
        v_lay.addWidget(top_frame, 0)
        v_lay.addWidget(middle_frame, 3)
        v_lay.addWidget(bottom_frame, 0)
        self.background.setLayout(v_lay)

        # Window
        drawer = QGridLayout()
        drawer.addWidget(self.background)
        drawer.setContentsMargins(0, 0, 0, 0)
        self.setLayout(drawer)

    def stylize_gui(self) -> None:
        self.setWindowTitle(self.text.get('title'))
        im_back: QPixmap = QPixmap(pt.pic_lobby_back)
        self.background.setPixmap(im_back)
        self.background.setScaledContents(True)
        self.setFixedSize(580, 500)
        with open(pt.qss_lobbywin, 'r') as css: self.setStyleSheet(css.read())

    def redo_text(self, lang: int) -> None:
        self.set_text(lang)
        self.lobby_name.setText(self.text.get('lobby_name'))
        self.information_text.setText(self.text.get('information'))
        self.setWindowTitle(self.text.get('title'))

    def connection_error_message(self, e: Exception) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(self.text.get('connection_error'))
        msg.setWindowTitle(self.text.get('connection_error_title')) 
        msg.setInformativeText(e.__str__())
        msg.exec_()

    def launch(self, name: str) -> None:
        print('intenté abrir lobby')
        self.p_name.setText(name)
        self.show()