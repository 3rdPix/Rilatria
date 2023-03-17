from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from ft.boxes import StatSet, ItemSet
from ft.board import Board
from ft.fun import hpad_this
from ft.styles import dialog_style, title_style_2, store_cell
import paths as pt

class GameWindow(QWidget):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setMinimumSize(800, 600)
        self.init_gui((1,))
        self.stylize_gui()

    def init_gui(self, data: tuple) -> None:
        
        self.background: QLabel = QLabel()
        

        layer1_opponent = self.player_2_panel()
        layer2_board = self.board_panel()
        layer3_playerpanel = self.player_1_panel()
        # layer3_cardspanel = self.cards_panel()
        layer4_storepanel = self.store_panel()

        v_lay = QVBoxLayout()

        layer1 = QHBoxLayout()
        layer1.addStretch(3)
        layer1.addWidget(layer1_opponent, 1)
        layer1.addStretch(3)
        v_lay.addLayout(layer1)

        layer2 = QHBoxLayout()
        layer2.addStretch(1)
        layer2.addWidget(layer2_board, 0)
        layer2.addStretch(1)
        v_lay.addLayout(layer2)

        layer3 = QHBoxLayout()
        layer3.addStretch(2)
        layer3.addWidget(layer3_playerpanel, 1)
        # layer3.addWidget(layer3_cardspanel, 1)
        layer3.addStretch(2)
        v_lay.addLayout(layer3)

        layer4 = QHBoxLayout()
        layer4.addStretch()
        layer4.addWidget(layer4_storepanel)
        layer4.addStretch()
        v_lay.addLayout(layer4)

        self.setLayout(v_lay)

        self.show()

 

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

        self.card2: QLabel = QLabel()
        self.card2.setScaledContents(True)

        self.card3: QLabel = QLabel()
        self.card3.setScaledContents(True)

        # Delete
        im_try = QPixmap(pt.im_try)
        self.card1.setPixmap(im_try)
        self.card2.setPixmap(im_try)
        self.card3.setPixmap(im_try)

        # Layouts and presentation
        internal = QHBoxLayout()
        internal.addWidget(self.card1)
        internal.addWidget(self.card2)
        internal.addWidget(self.card3)
        cards_panel.setLayout(internal)
        return cards_panel

    """
    Revisited
    """
    
    def board_panel(self) -> QGroupBox:
        box = QGroupBox(title='Battle Field')
        grid = QGridLayout()
        self.board = Board()
        grid.addWidget(self.board)
        box.setLayout(grid)
        return box  

    def store_panel(self) -> QGroupBox:
        store: QGroupBox = QGroupBox(title='Store')

        pawn = ItemSet(pt.im_pawn, 'Bárbaro', pt.im_item_back,
                       pt.im_item_hover, pt.im_item_click)
        horse = ItemSet(pt.im_horse, 'Jinete', pt.im_item_back,
                        pt.im_item_hover, pt.im_item_click)
        bishop = ItemSet(pt.im_bishop, 'Lancero', pt.im_item_back,
                         pt.im_item_hover, pt.im_item_click)
        rook = ItemSet(pt.im_rook, 'Armatoste', pt.im_item_back,
                       pt.im_item_hover, pt.im_item_click)
        joker = ItemSet(pt.im_joker, 'Asesino', pt.im_item_back,
                        pt.im_item_hover, pt.im_item_click)

        # total layout
        int_lay = QHBoxLayout()
        int_lay.addWidget(pawn)
        int_lay.addWidget(horse)
        int_lay.addWidget(bishop)
        int_lay.addWidget(rook)
        int_lay.addWidget(joker)

        store.setLayout(int_lay)
        return store
    
    def player_2_panel(self) -> QGroupBox:
        self.p2anel: QGroupBox = QGroupBox(title='Player 2')
        
        self.p2_HP = StatSet(pt.im_heart, pt.im_stat_frame)
        self.p2_VP = StatSet(pt.im_shield, pt.im_stat_frame)
        self.p2_LP = StatSet(pt.im_clover, pt.im_stat_frame)
        self.p2_CP = StatSet(pt.im_coin, pt.im_stat_frame)

        # Panel layout
        lay_p2 = QHBoxLayout()
        lay_p2.addLayout(self.p2_HP)
        lay_p2.addLayout(self.p2_VP)
        lay_p2.addLayout(self.p2_LP)
        lay_p2.addLayout(self.p2_CP)

        self.p2anel.setLayout(lay_p2)
        return self.p2anel
    
    def player_1_panel(self) -> QGroupBox:
        self.p1anel: QGroupBox = QGroupBox(title='Player 1')
        
        self.p1_HP = StatSet(pt.im_heart, pt.im_stat_frame)
        self.p1_VP = StatSet(pt.im_shield, pt.im_stat_frame)
        self.p1_LP = StatSet(pt.im_clover, pt.im_stat_frame)
        self.p1_CP = StatSet(pt.im_coin, pt.im_stat_frame)

        # Panel layout
        lay_p1 = QHBoxLayout()
        lay_p1.addLayout(self.p1_HP)
        lay_p1.addLayout(self.p1_VP)
        lay_p1.addLayout(self.p1_LP)
        lay_p1.addLayout(self.p1_CP)

        self.p1anel.setLayout(lay_p1)
        return self.p1anel