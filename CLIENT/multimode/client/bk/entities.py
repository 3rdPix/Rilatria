from PyQt5.QtCore import QObject, pyqtSignal
from random import randint as rint


class Player(QObject):

    def __init__(self, stats: tuple, tl_death: pyqtSignal) -> None:
        super().__init__()
        self.name, self._health, self._honor, self._luck, self._coins = stats
        self.sg_death: pyqtSignal = tl_death

    def get_health(self): return self._health
    def set_health(self, new_val):
        if new_val < 0:
            self._health = 0
            self.sg_death.emit()
        elif new_val > 10: self._health = 10
        else: self._health = new_val
    health = property(get_health, set_health)

    def get_honor(self): return self._honor
    def set_honor(self, new_val):
        if new_val < 0: self._honor = 0
        elif new_val > 10: self._honor = 10
        else: self._honor = new_val
    honor = property(get_honor, set_honor)

    def get_luck(self): return self._luck
    def set_luck(self, new_val):
        if new_val < 0: self._luck = 0
        elif new_val > 10: self._luck = 10
        else: self._luck = new_val
    luck = property(get_luck, set_luck)

    def get_coins(self): return self._coins
    def set_coins(self, new_val):
        if new_val < 0: self._coins = 0
        elif new_val > 10: self._coins = 10
        else: self._coins = new_val
    coins = property(get_coins, set_coins)

    def reserve_effects(self) -> None:
        if self.health > 5: self.coins -= 1
        if self.honor > 5:
            self.health += 1
            if self.honor == 10: self.health += 1
        if self.luck > 5:
            if rint(1, 2) == 1:
                self.coins += 1
                if self.luck == 10: self.health += 1
            else: self.health -= 1
        if self.coins > 5: self.honor -= 1

    def is_alive(self) -> bool:
        if self.health < 1: return False
        return True


class Board(QObject):

    def __init__(self, **kwargs) -> None:
        super().__init__(*kwargs)
        self.on_board: list = list()

    def is_empty(self) -> bool:
        pass


class Piece(QObject):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Card:
    vida: int = 0
    honor: int = 0
    suerte: int = 0
    dinero: int = 0


class Deck(QObject):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @staticmethod
    def draw(number: int) -> set:
        cards: set = set()
        for _ in range(number):
            new_card = Card()
            element1 = rint(1, 4)
            val1 = rint(-3, 3)
            match element1:
                case 1: new_card.vida = val1
                case 2: new_card.honor = val1
                case 3: new_card.suerte = val1
                case 4: new_card.dinero = val1
            
            element2 = rint(1, 4)
            while element1 == element2: element2 = rint(1, 4)
            if val1 > 0: val2 = rint(-3, 0)
            elif val1 <= 0: val2 = rint(0, 3)
            match element2:
                case 1: new_card.vida = val2
                case 2: new_card.honor = val2
                case 3: new_card.suerte = val2
                case 4: new_card.dinero = val2
            cards.add(new_card)
        return cards