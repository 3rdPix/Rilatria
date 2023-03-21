from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from ft.boxes import StatSet, ItemSet
from ft.board import Board
import paths as pt
import json

class GameWindow(QWidget):

    def __init__(self, lang: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_text(lang)
        self.init_gui()
        self.stylize_gui()

    def set_text(self, lang: int) -> None:
        match lang:
            case 0: file = pt.lang_eng
            case 1: file = pt.lang_spa
            case 2: file = pt.lang_fre
        with open(file, 'r', encoding='utf-8') as raw:
            self.text = json.load(raw).get('game_win')

    def init_gui(self) -> None:
        self.background: QLabel = QLabel(parent=self)
        self.setMinimumSize(1050, 690)

        # We save these to update players names
        self.p1anel = self.player_1_panel()
        self.p2anel = self.player_2_panel()

        # No need to save these
        self.board_panel: QGroupBox = self.board_panel()
        self.cards_panel: QGroupBox = self.cards_panel()
        self.store_panel: QGroupBox = self.store_panel()

        # Window disrtribution
        grid = QGridLayout()
        grid.addWidget(self.p1anel, 1, 1, 8, 1)
        grid.addWidget(self.board_panel, 1, 2, 6, 6)
        grid.addWidget(self.p2anel, 1, 8, 8, 1)
        grid.addWidget(self.store_panel, 7, 2, 2, 4)
        grid.addWidget(self.cards_panel, 7, 6, 2, 2)

        self.background.setLayout(grid)
        self.background.setFixedSize(self.size())

    def redo_text(self, lang: int) -> None:
        self.set_text(lang)
        self.board_panel.setTitle(self.text.get('field'))
        self.cards_panel.setTitle(self.text.get('cards'))
        self.store_panel.setTitle(self.text.get('store'))
        self.item1.redo_text(self.text.get('item1'))
        self.item2.redo_text(self.text.get('item2'))
        self.item3.redo_text(self.text.get('item3'))
        self.item4.redo_text(self.text.get('item4'))
        self.item5.redo_text(self.text.get('item5'))

    def stylize_gui(self) -> None:
        im_back: QPixmap = QPixmap(pt.pic_gamewin_back)
        self.background.setPixmap(im_back)
        self.background.setScaledContents(True)

        with open(pt.qss_gamewin, 'r') as raw: style = raw.read()
        self.setStyleSheet(style)

    def cards_panel(self) -> QGroupBox:

        cards_panel = QGroupBox(title=self.text.get('cards'))

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
        im_try = QPixmap(pt.pic_try)
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
        box = QGroupBox(title=self.text.get('field'))
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
        store: QGroupBox = QGroupBox(title=self.text.get('store'))
        store.setMinimumSize(510, 130)

        self.item1 = ItemSet(pt.pic_pawn, self.text.get('item1'), pt.pic_item_back,
                       pt.pic_item_hover, pt.pic_item_click)
        self.item2 = ItemSet(pt.pic_horse, self.text.get('item2'), pt.pic_item_back,
                        pt.pic_item_hover, pt.pic_item_click)
        self.item3 = ItemSet(pt.pic_bishop, self.text.get('item3'), pt.pic_item_back,
                         pt.pic_item_hover, pt.pic_item_click)
        self.item4 = ItemSet(pt.pic_rook, self.text.get('item4'), pt.pic_item_back,
                       pt.pic_item_hover, pt.pic_item_click)
        self.item5 = ItemSet(pt.pic_joker, self.text.get('item5'), pt.pic_item_back,
                        pt.pic_item_hover, pt.pic_item_click)

        # total layout
        int_lay = QHBoxLayout()
        int_lay.addStretch(5)
        int_lay.addWidget(self.item1)
        int_lay.addStretch(1)
        int_lay.addWidget(self.item2)
        int_lay.addStretch(1)
        int_lay.addWidget(self.item3)
        int_lay.addStretch(1)
        int_lay.addWidget(self.item4)
        int_lay.addStretch(1)
        int_lay.addWidget(self.item5)
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
        
        self.p2_HP = StatSet(pt.pic_heart, pt.pic_stat_frame)
        self.p2_VP = StatSet(pt.pic_shield, pt.pic_stat_frame)
        self.p2_LP = StatSet(pt.pic_clover, pt.pic_stat_frame)
        self.p2_CP = StatSet(pt.pic_coin, pt.pic_stat_frame)

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
        
        self.p1_HP = StatSet(pt.pic_heart, pt.pic_stat_frame)
        self.p1_VP = StatSet(pt.pic_shield, pt.pic_stat_frame)
        self.p1_LP = StatSet(pt.pic_clover, pt.pic_stat_frame)
        self.p1_CP = StatSet(pt.pic_coin, pt.pic_stat_frame)

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