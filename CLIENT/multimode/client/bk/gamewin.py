from PyQt5.QtCore import QObject, pyqtSignal
from bk.entities import Player, Board, Piece, Deck


class Ronda(QObject):

    def __init__(self, p1: Player, p2: Player, brd: Board, dk:Deck) -> None:
        super().__init__()
        self.p1: p1
        self.p2: p2
        self.brd: Board = brd
        self.dk: Deck = dk
        self._current_turn: int = 0

    def run(self) -> None:
        pass 



class GameWinLog(QObject):

    sg_starting_data = pyqtSignal(tuple)
    sg_drawn_cards = pyqtSignal(set)

    tl_player_death = pyqtSignal(str)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.define_properties()
        self.board: Board = Board()

    def define_properties(self) -> None:
        self.current_turn: bool = True # 1: true, 2: false
        self.turn_counter: int = 1
        self.active_game: bool = True

    def receive_start(self, username: str) -> None:
        # self.sg_starting_data.emit(data)
        # p1, p2, health, honor, luck, coins = data
        # self.p1: Player = Player((p1, health, honor, luck, coins), 
        #                          self.tl_player_death)
        # self.p2: Player = Player((p2, health, honor, luck, coins),
        #                          self.tl_player_death)
        
        # self.start_game()
        pass

    """
    Respecto al inicio del juego, primero será implementada enteramente
    la sección de las cartas y sus efectos de reserva, para luego integrar
    tardíamente el tablero
    """

    def start_game(self) -> None:
        while self.active_game:
            self.cards_play()
            self.current_turn = not self.current_turn
            self.turn_counter += 1

    def cards_play(self) -> None:
        drawn: set = Deck.draw(3)
        self.sg_drawn_cards.emit(drawn)