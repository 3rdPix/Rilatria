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

    tl_player_death = pyqtSignal(str)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.board: Board = Board()

    def receive_start(self, data: tuple) -> None:
        self.sg_starting_data.emit(data)
        p1, p2, health, honor, luck, coins = data
        self.p1: Player = Player((p1, health, honor, luck, coins), 
                                 self.tl_player_death)
        self.p2: Player = Player((p2, health, honor, luck, coins),
                                 self.tl_player_death)
        
        self.start_game()

    def start_game(self) -> None:
        pass