from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel
from PyQt5.QtGui import QPixmap
from ft.board import Board
from ft.fun import hpad_this
import paths as pt

class GameWindow(QWidget):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.init_gui()

    def init_gui(self) -> None:
        left = self.player_1_panel()
        middle = self.middle_panel()
        right = self.player_2_panel()
        total = QHBoxLayout()
        total.addWidget(left, 0)
        total.addLayout(middle, 1)
        total.addWidget(right, 0)
        self.setLayout(total)

    def player_1_panel(self) -> QGroupBox:
        panel: QGroupBox = QGroupBox(title='Player 1')
        
        # Player 1 status
        self.p1_HP: QLabel = QLabel(text='0')
        self.p1_VP: QLabel = QLabel(text='0')
        self.p1_LP: QLabel = QLabel(text='0')
        self.p1_CP: QLabel = QLabel(text='0')
        
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

        panel.setLayout(lay_p1)
        return panel

    def middle_panel(self) -> QVBoxLayout:
        panel: QVBoxLayout = QVBoxLayout()
        self.board: Board = Board()
        panel.addWidget(self.board)
        return panel

    def player_2_panel(self) -> QGroupBox:
        panel: QGroupBox = QGroupBox(title='Player 2')
        
        # Player 1 status
        self.p2_HP: QLabel = QLabel(text='0')
        self.p2_VP: QLabel = QLabel(text='0')
        self.p2_LP: QLabel = QLabel(text='0')
        self.p2_CP: QLabel = QLabel(text='0')
        
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

        panel.setLayout(lay_p2)
        return panel