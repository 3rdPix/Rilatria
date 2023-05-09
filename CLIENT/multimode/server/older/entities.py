from dataclasses import dataclass
from socket import socket
from threading import Lock
from random import randint as rint


@dataclass
class User:
    ip: str
    wire: socket
    controller: Lock = Lock()
    username: str = None
    player = None
    sv_listen = True

    def __repr__(self) -> str:
        return f'Player {self.username}'
    
class Player:
    
    def __init__(self, ant_death) -> None:
        self.death = ant_death
        self._health: int = 6
        self._honor: int = 2
        self._luck: int = 2
        self._coins: int = 2

    def is_alive(self) -> bool:
        if self.health < 1: return False
        if self.coins < 1 and self.luck < 1: return False
        return True
    
    def won(self) -> bool:
        if self.health == 10 and self.luck == 10: return True
        if self.honor == 10 and self.coins == 10: return True
        return False
    
    def get_health(self): return self._health
    def set_health(self, new_val):
        if new_val < 0: self._health = 0
        elif new_val > 10: self._health = 10
        else: self._health = new_val
    health = property(get_health, set_health)

    def get_honor(self): return self._honor
    def set_honor(self, new_val):
        if new_val < 0: self._honor4 = 0
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

    def chain_effects(self) -> None:
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

class Card:
    health: int = 0
    honor: int = 0
    luck: int = 0
    coins: int = 0


class Deck:

    @staticmethod
    def draw(number: int) -> tuple:
        cards: list = list()
        for times in range(number): cards.append(Deck.get_new_card())
        return tuple(cards)
    
    @staticmethod
    def get_new_card() -> Card:
        new_card = Card()
        element1 = rint(1, 4)
        val1 = rint(-3, 3)
        match element1:
            case 1: new_card.health = val1
            case 2: new_card.honor = val1
            case 3: new_card.luck = val1
            case 4: new_card.coins = val1
        
        element2 = rint(1, 4)
        while element1 == element2: element2 = rint(1, 4)
        if val1 > 0: val2 = rint(-3, 0)
        elif val1 <= 0: val2 = rint(0, 3)
        match element2:
            case 1: new_card.health = val2
            case 2: new_card.honor = val2
            case 3: new_card.luck = val2
            case 4: new_card.coins = val2
        return new_card
    