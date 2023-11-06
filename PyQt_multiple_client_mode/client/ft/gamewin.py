from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,\
    QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from ft.boxes import StatSet, ItemSet, TurnSet, CardSet
from ft.board import Board
import paths as pt
import json

class GameWindow(QWidget):

    sg_card_picked = pyqtSignal(int)
    sg_cell_clicked = pyqtSignal(tuple)
    sg_item_clicked_to_buy = pyqtSignal(str)

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
        self.setMinimumSize(1169, 690)

        # We save these to update players names
        self.p1anel = self.player_1_panel()
        self.p2anel = self.player_2_panel()

        # No need to save these
        self.board_panel: QGroupBox = self.create_board_panel()
        self.cards_panel: QGroupBox = self.create_cards_panel()
        self.store_panel: QGroupBox = self.create_store_panel()
        self.turn_panel: QGroupBox = self.create_turn_panel()

        # Window disrtribution
        windows_layout = QHBoxLayout()
        windows_layout.addWidget(self.p1anel)
        windows_layout.addStretch()
        
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.board_panel)
        
        center_bot_layout = QHBoxLayout()
        center_bot_layout.addWidget(self.store_panel)
        center_bot_layout.addStretch()
        center_bot_layout.addWidget(self.cards_panel)
        center_bot_layout.addStretch()
        center_bot_layout.addWidget(self.turn_panel)
        center_layout.addLayout(center_bot_layout)
        windows_layout.addLayout(center_layout)

        windows_layout.addStretch()
        windows_layout.addWidget(self.p2anel)
        

        # row, col, row_s, col_s
        # grid = QGridLayout()
        # grid.addWidget(self.p1anel, 1, 1, 8, 1)
        # grid.addWidget(self.board_panel, 1, 2, 6, 7)
        # grid.addWidget(self.p2anel, 1, 9, 8, 1)
        # grid.addWidget(self.store_panel, 7, 2, 2, 4)
        # grid.addWidget(self.cards_panel, 7, 6, 2, 2)
        # grid.addWidget(self.turn_panel, 8, 8, 2, 1)

        self.background.setLayout(windows_layout)
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

    def create_cards_panel(self) -> QGroupBox:

        cards_panel = QGroupBox(title=self.text.get('cards'))

        # Cards
        self.card1 = CardSet(
            pt.pic_try,
            pt.pic_heart,
            pt.pic_shield,
            pt.pic_clover,
            pt.pic_coin,
            0, self.sg_card_picked)
        self.card1.setFixedSize(81, 121)

        self.card2 = CardSet(
            pt.pic_try,
            pt.pic_heart,
            pt.pic_shield,
            pt.pic_clover,
            pt.pic_coin,
            1, self.sg_card_picked)
        self.card2.setFixedSize(81, 121)

        self.card3 = CardSet(
            pt.pic_try,
            pt.pic_heart,
            pt.pic_shield,
            pt.pic_clover,
            pt.pic_coin,
            2, self.sg_card_picked)
        self.card3.setFixedSize(81, 121)

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
    
    def create_turn_panel(self) -> QGroupBox:
        v_box = QVBoxLayout()
        self.btn = TurnSet(self.text.get('end_turn'), pt.pic_turn_back,
                      pt.pic_turn_hover, pt.pic_turn_press)
        # total
        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.btn)
        h_box.addStretch()

        v_box.addStretch()
        v_box.addLayout(h_box)
        v_box.addStretch()

        box = QGroupBox()
        box.setLayout(v_box)
        box.setMaximumWidth(115)
        return box

    def create_board_panel(self) -> QGroupBox:
        box = QGroupBox(title=self.text.get('field'))
        self.board = Board(
            im_barbarian=pt.pic_pawn,
            im_horserider=pt.pic_horse,
            im_spearman=pt.pic_bishop,
            im_rattletrap=pt.pic_rook,
            im_joker=pt.pic_joker,
            im_hero=pt.pic_p1,
            sg_cell_clicked=self.sg_cell_clicked
        )
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

    def create_store_panel(self) -> QGroupBox:
        store: QGroupBox = QGroupBox(title=self.text.get('store'))
        store.setMinimumSize(510, 130)

        self.item1 = ItemSet(pt.pic_pawn, self.text.get('item1'), pt.pic_item_back,
                       pt.pic_item_hover, pt.pic_item_click,
                       self.sg_item_clicked_to_buy, name_id='Barbarian')
        self.item2 = ItemSet(pt.pic_horse, self.text.get('item2'), pt.pic_item_back,
                        pt.pic_item_hover, pt.pic_item_click,
                        self.sg_item_clicked_to_buy, name_id='Horserider')
        self.item3 = ItemSet(pt.pic_bishop, self.text.get('item3'), pt.pic_item_back,
                         pt.pic_item_hover, pt.pic_item_click,
                         self.sg_item_clicked_to_buy, name_id='Spearman')
        self.item4 = ItemSet(pt.pic_rook, self.text.get('item4'), pt.pic_item_back,
                       pt.pic_item_hover, pt.pic_item_click,
                       self.sg_item_clicked_to_buy, name_id='RattleTrap')
        self.item5 = ItemSet(pt.pic_joker, self.text.get('item5'), pt.pic_item_back,
                        pt.pic_item_hover, pt.pic_item_click,
                        self.sg_item_clicked_to_buy, name_id='Joker')

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

    def resizeEvent(self, event) -> None:
        self.background.setFixedSize(self.size())
        return super().resizeEvent(event)
    
    """
    Reception
    """
    def my_name(self, name: str) -> None:
        self.p1anel.setTitle(name)

    def opponent_name(self, name: str) -> None:
        self.p2anel.setTitle(name)

    def my_turn(self, my: bool) -> None:
        self.btn.setEnabled(my)

    def stat_update(self, details: dict) -> None:
        val = details.get('new_val')
        if details.get('mine'):
            match details.get('stat'):
                case 'health': self.p1_HP.set_value(val)
                case 'honor': self.p1_VP.set_value(val)
                case 'luck': self.p1_LP.set_value(val)
                case 'coins': self.p1_CP.set_value(val)
        else:
            match details.get('stat'):
                case 'health': self.p2_HP.set_value(val)
                case 'honor': self.p2_VP.set_value(val)
                case 'luck': self.p2_LP.set_value(val)
                case 'coins': self.p2_CP.set_value(val)

    def update_board(self, board: list) -> None:
        self.board.display(board)

    def update_legal_moves(self, options: list) -> None:
        self.board.show_legal_moves(options)

    def update_legal_eats(self, options: list) -> None:
        self.board.show_legal_eats(options)

    def receive_card(self, options: list) -> None:
        top_1, bot_1, top_2, bot_2, top_3, bot_3 = options
        self.card1.set_top(str(top_1[1]), top_1[0])
        self.card1.set_bot(str(bot_1[1]), bot_1[0])
        self.card2.set_top(str(top_2[1]), top_2[0])
        self.card2.set_bot(str(bot_2[1]), bot_2[0])
        self.card3.set_top(str(top_3[1]), top_3[0])
        self.card3.set_bot(str(bot_3[1]), bot_3[0])