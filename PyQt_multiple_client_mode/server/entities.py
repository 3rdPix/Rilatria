from socket import socket
from threading import Lock
from random import randint as rint

class Player:
    
    def __init__(self, ant_death) -> None:
        self.death = ant_death
        self._health: int = 6
        self._honor: int = 2
        self._luck: int = 2
        self._coins: int = 2
        self.my_turn: bool = False

    """
    PUBLIC
    """
    def is_alive(self) -> bool:
        if self.health < 1: return False
        if self.coins < 1 and self.luck < 1: return False
        return True
    
    """
    PROPERTIES
    """
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

    """
    METHODS
    """
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


class User(Player):

    def __init__(self, wire: socket, id: int) -> None:
        super().__init__(print)
        self.wire: socket = wire
        self.id: int = id
        self.controller: Lock = Lock()
        self.user_name: str = ''

    def __str__(self) -> str:
        return f'User {self.id}:{self.user_name}' if self.user_name != '' else \
        f'User {self.id}:NaN'
    
    def __repr__(self) -> str:
        return self.__str__()