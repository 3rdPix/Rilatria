from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ft.boxes import StatSet, ItemSet
from ft.board import Board
from ft.fun import hpad_this
from ft.styles import dialog_style, title_style_2, store_cell
import paths as pt

class GameWindow(QWidget):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.init_gui()
        self.stylize_gui()

    def init_gui(self) -> None:
        self.background: QLabel = QLabel(parent=self)
        self.setMinimumSize(1050, 690)

        # We save these to update players names
        self.p1anel = self.player_1_panel()
        self.p2anel = self.player_2_panel()

        # No need to save these
        board_panel = self.board_panel()
        cards_panel = self.cards_panel()
        store_panel = self.store_panel()

        # Window disrtribution
        grid = QGridLayout()
        grid.addWidget(self.p1anel, 1, 1, 8, 1)
        grid.addWidget(board_panel, 1, 2, 6, 6)
        grid.addWidget(self.p2anel, 1, 8, 8, 1)
        grid.addWidget(store_panel, 7, 2, 2, 4)
        grid.addWidget(cards_panel, 7, 6, 2, 2)

        self.background.setLayout(grid)
        self.background.setFixedSize(self.size())

    def stylize_gui(self) -> None:
        im_back: QPixmap = QPixmap(pt.im_gamewin_back)
        self.background.setPixmap(im_back)
        self.background.setScaledContents(True)

        with open(pt.css_gamewin, 'r') as raw: style = raw.read()
        self.setStyleSheet(style)

    def cards_panel(self) -> QGroupBox:

        cards_panel = QGroupBox(title='Cards')

        # Cards
        self.card1: QLabel = QLabel()
        self.card1.setScaledContents(True)
        self.card1.setFixedSize(81, 121)

        self.card2: QLabel = QLabel()
        self.card2.setScaledContents(True)
        self.card2.setFixedSize(81, 121)

        self.card3: QLabel = QLabel()
        self.card3.setScaledContents(True)
        self.card3.setFixedSize(81, 121)

        # Delete
        im_try = QPixmap(pt.im_try)
        self.card1.setPixmap(im_try)
        self.card2.setPixmap(im_try)
        self.card3.setPixmap(im_try)

        # Layouts and presentation
        int_lay = QHBoxLayout()
        int_lay.addStretch()
        int_lay.addWidget(self.card1)
        int_lay.addStretch()
        int_lay.addWidget(self.card2)
        int_lay.addStretch()
        int_lay.addWidget(self.card3)
        int_lay.addStretch()

        ext_lay = QVBoxLayout()
        ext_lay.addStretch()
        ext_lay.addLayout(int_lay)
        ext_lay.addStretch()
        cards_panel.setLayout(ext_lay)
        return cards_panel
    
    def board_panel(self) -> QGroupBox:
        box = QGroupBox(title='Battle Field')
        self.board = Board()
        v_box = QVBoxLayout()
        v_box.addStretch()

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.board)
        h_box.addStretch()
        v_box.addLayout(h_box)

        v_box.addStretch()
        
        box.setLayout(v_box)
        return box 

    def store_panel(self) -> QGroupBox:
        store: QGroupBox = QGroupBox(title='Store')
        store.setMinimumSize(510, 130)

        self.pawn = ItemSet(pt.im_pawn, 'Bárbaro', pt.im_item_back,
                       pt.im_item_hover, pt.im_item_click)
        self.horse = ItemSet(pt.im_horse, 'Jinete', pt.im_item_back,
                        pt.im_item_hover, pt.im_item_click)
        self.bishop = ItemSet(pt.im_bishop, 'Lancero', pt.im_item_back,
                         pt.im_item_hover, pt.im_item_click)
        self.rook = ItemSet(pt.im_rook, 'Armatoste', pt.im_item_back,
                       pt.im_item_hover, pt.im_item_click)
        self.joker = ItemSet(pt.im_joker, 'Asesino', pt.im_item_back,
                        pt.im_item_hover, pt.im_item_click)

        # total layout
        int_lay = QHBoxLayout()
        int_lay.addStretch(5)
        int_lay.addWidget(self.pawn)
        int_lay.addStretch(1)
        int_lay.addWidget(self.horse)
        int_lay.addStretch(1)
        int_lay.addWidget(self.bishop)
        int_lay.addStretch(1)
        int_lay.addWidget(self.rook)
        int_lay.addStretch(1)
        int_lay.addWidget(self.joker)
        int_lay.addStretch(5)

        ext_lay = QVBoxLayout()
        ext_lay.addStretch()
        ext_lay.addLayout(int_lay)
        ext_lay.addStretch()

        store.setLayout(ext_lay)
        return store
    
    def player_2_panel(self) -> QGroupBox:
        p2anel: QGroupBox = QGroupBox(title='Player 2')
        p2anel.setMaximumWidth(115)
        
        self.p2_HP = StatSet(pt.im_heart, pt.im_stat_frame)
        self.p2_VP = StatSet(pt.im_shield, pt.im_stat_frame)
        self.p2_LP = StatSet(pt.im_clover, pt.im_stat_frame)
        self.p2_CP = StatSet(pt.im_coin, pt.im_stat_frame)

        # Panel layout
        lay_p2 = QVBoxLayout()
        lay_p2.addLayout(self.p2_HP)
        lay_p2.addLayout(self.p2_VP)
        lay_p2.addLayout(self.p2_LP)
        lay_p2.addLayout(self.p2_CP)

        p2anel.setLayout(lay_p2)
        return p2anel
    
    def player_1_panel(self) -> QGroupBox:
        p1anel: QGroupBox = QGroupBox(title='Player 1')
        p1anel.setMaximumWidth(115)
        
        self.p1_HP = StatSet(pt.im_heart, pt.im_stat_frame)
        self.p1_VP = StatSet(pt.im_shield, pt.im_stat_frame)
        self.p1_LP = StatSet(pt.im_clover, pt.im_stat_frame)
        self.p1_CP = StatSet(pt.im_coin, pt.im_stat_frame)

        # Panel layout
        lay_p1 = QVBoxLayout()
        lay_p1.addLayout(self.p1_HP)
        lay_p1.addLayout(self.p1_VP)
        lay_p1.addLayout(self.p1_LP)
        lay_p1.addLayout(self.p1_CP)

        p1anel.setLayout(lay_p1)
        return p1anel
    
    def launch(self, username: str) -> None:
        self.p1anel.setTitle(username)
        self.show()

    def resizeEvent(self, event) -> None:
        self.background.setFixedSize(self.size())
        return super().resizeEvent(event)