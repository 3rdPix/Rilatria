from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel
from PyQt5.QtGui import QPixmap
from ft.board import Board
from ft.fun import hpad_this
from ft.styles import dialog_style, title_style_2
import paths as pt

class GameWindow(QWidget):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setMinimumSize(800, 600)

    def init_gui(self, data: tuple) -> None:
        left = self.player_1_panel()
        middle = self.middle_panel()
        right = self.player_2_panel()
        total = QHBoxLayout()
        total.addWidget(left, 0)
        total.addLayout(middle, 1)
        total.addWidget(right, 0)
        self.setLayout(total)
        self.p1anel.setTitle(data[0])
        self.p2anel.setTitle(data[1])
        self.p1_HP.setText(data[2])
        self.p2_HP.setText(data[2])
        self.p1_VP.setText(data[3])
        self.p2_VP.setText(data[3])
        self.p1_LP.setText(data[4])
        self.p2_LP.setText(data[4])
        self.p1_CP.setText(data[5])
        self.p2_CP.setText(data[5])
        self.show()

    def player_1_panel(self) -> QGroupBox:
        self.p1anel: QGroupBox = QGroupBox(title='Player 1')
        self.p1anel.setStyleSheet(title_style_2)

        # Player 1 status
        self.p1_HP: QLabel = QLabel(text='0')
        self.p1_HP.setStyleSheet(dialog_style)
        self.p1_VP: QLabel = QLabel(text='0')
        self.p1_VP.setStyleSheet(dialog_style)
        self.p1_LP: QLabel = QLabel(text='0')
        self.p1_LP.setStyleSheet(dialog_style)
        self.p1_CP: QLabel = QLabel(text='0')
        self.p1_CP.setStyleSheet(dialog_style)
        
        # Icons
        im_heart: QPixmap = QPixmap(pt.im_heart)
        heart: QLabel = QLabel()
        heart.setPixmap(im_heart)
        heart.setFixedSize(80, 80)
        heart.setScaledContents(True)

        im_shield: QPixmap = QPixmap(pt.im_shield)
        shield: QLabel = QLabel()
        shield.setPixmap(im_shield)
        shield.setFixedSize(80, 80)
        shield.setScaledContents(True)

        im_clover: QPixmap = QPixmap(pt.im_clover)
        clover: QLabel = QLabel()
        clover.setPixmap(im_clover)
        clover.setFixedSize(80, 80)
        clover.setScaledContents(True)

        im_coin: QPixmap = QPixmap(pt.im_coin)
        coin: QLabel = QLabel()
        coin.setPixmap(im_coin)
        coin.setFixedSize(80, 80)
        coin.setScaledContents(True)

        # Lower layouts
        lay_hp: QVBoxLayout = hpad_this(
            heart,
            self.p1_HP
        )
        lay_vp: QVBoxLayout = hpad_this(
            shield,
            self.p1_VP
        )
        lay_lp: QVBoxLayout = hpad_this(
            clover,
            self.p1_LP
        )
        lay_cp: QVBoxLayout = hpad_this(
            coin,
            self.p1_CP
        )

        # Panel layout
        lay_p1: QVBoxLayout = QVBoxLayout()
        lay_p1.addStretch()
        lay_p1.addLayout(lay_hp)
        lay_p1.addStretch()
        lay_p1.addLayout(lay_vp)
        lay_p1.addStretch()
        lay_p1.addLayout(lay_lp)
        lay_p1.addStretch()
        lay_p1.addLayout(lay_cp)
        lay_p1.addStretch()

        self.p1anel.setLayout(lay_p1)
        return self.p1anel

    def middle_panel(self) -> QVBoxLayout:
        
        self.board: Board = Board()
        lay_b = hpad_this(self.board)
        return lay_b

    def player_2_panel(self) -> QGroupBox:
        self.p2anel: QGroupBox = QGroupBox(title='Player 2')
        self.p2anel.setStyleSheet(title_style_2)
        
        # Player 1 status
        self.p2_HP: QLabel = QLabel(text='0')
        self.p2_HP.setStyleSheet(dialog_style)
        self.p2_VP: QLabel = QLabel(text='0')
        self.p2_VP.setStyleSheet(dialog_style)
        self.p2_LP: QLabel = QLabel(text='0')
        self.p2_LP.setStyleSheet(dialog_style)
        self.p2_CP: QLabel = QLabel(text='0')
        self.p2_CP.setStyleSheet(dialog_style)
        
        # Icons
        im_heart: QPixmap = QPixmap(pt.im_heart)
        heart: QLabel = QLabel()
        heart.setPixmap(im_heart)
        heart.setFixedSize(80, 80)
        heart.setScaledContents(True)

        im_shield: QPixmap = QPixmap(pt.im_shield)
        shield: QLabel = QLabel()
        shield.setPixmap(im_shield)
        shield.setFixedSize(80, 80)
        shield.setScaledContents(True)

        im_clover: QPixmap = QPixmap(pt.im_clover)
        clover: QLabel = QLabel()
        clover.setPixmap(im_clover)
        clover.setFixedSize(80, 80)
        clover.setScaledContents(True)

        im_coin: QPixmap = QPixmap(pt.im_coin)
        coin: QLabel = QLabel()
        coin.setPixmap(im_coin)
        coin.setFixedSize(80, 80)
        coin.setScaledContents(True)

        # Lower layouts
        lay_hp: QVBoxLayout = hpad_this(
            heart,
            self.p2_HP
        )
        lay_vp: QVBoxLayout = hpad_this(
            shield,
            self.p2_VP
        )
        lay_lp: QVBoxLayout = hpad_this(
            clover,
            self.p2_LP
        )
        lay_cp: QVBoxLayout = hpad_this(
            coin,
            self.p2_CP
        )

        # Panel layout
        lay_p2: QVBoxLayout = QVBoxLayout()
        lay_p2.addStretch()
        lay_p2.addLayout(lay_hp)
        lay_p2.addStretch()
        lay_p2.addLayout(lay_vp)
        lay_p2.addStretch()
        lay_p2.addLayout(lay_lp)
        lay_p2.addStretch()
        lay_p2.addLayout(lay_cp)
        lay_p2.addStretch()

        self.p2anel.setLayout(lay_p2)
        return self.p2anel