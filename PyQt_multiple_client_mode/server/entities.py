from socket import socket
from threading import Lock
from random import randint as rint

class Player:
    
    def __init__(self, ant_death, parameters) -> None:
        self.death = ant_death
        self.parameters = parameters
        self.create_variables()

    def create_variables(self) -> None:
        self._health: int = self.parameters.get('init_health')
        self._honor: int = self.parameters.get('init_honor')
        self._luck: int = self.parameters.get('init_luck')
        self._coins: int = self.parameters.get('init_coins')
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
        elif new_val > self.parameters.get('max_health'):
            self._health = self.parameters.get('max_health')
        else: self._health = new_val
    health = property(get_health, set_health)

    def get_honor(self): return self._honor
    def set_honor(self, new_val):
        if new_val < 0: self._honor4 = 0
        elif new_val > self.parameters.get('max_honor'):
            self._honor = self.parameters.get('max_honor')
        else: self._honor = new_val
    honor = property(get_honor, set_honor)

    def get_luck(self): return self._luck
    def set_luck(self, new_val):
        if new_val < 0: self._luck = 0
        elif new_val > self.parameters.get('max_luck'):
            self._luck = self.parameters.get('max_luck')
        else: self._luck = new_val
    luck = property(get_luck, set_luck)

    def get_coins(self): return self._coins
    def set_coins(self, new_val):
        if new_val < 0: self._coins = 0
        elif new_val > self.parameters.get('max_coins'):
            self._coins = self.parameters.get('max_coins')
        else: self._coins = new_val
    coins = property(get_coins, set_coins)

    """
    METHODS
    """
    def chain_effects(self) -> None:
        if self.health > self.parameters.get('limit_health'):
            self.coins -= self.parameters.get('loss_coins_by_health')
        if self.honor > self.parameters.get('limit_honor'):
            self.health += self.parameters.get('gain_health_by_honor')
            if self.honor == self.parameters.get('max_honor'):
                self.health += self.parameters.get('gain_health_by_honor')
        if self.luck > self.parameters.get('limit_luck'):
            if rint(1, 2) == 1:
                self.coins += self.parameters.get('gain_coins_by_luck')
                if self.luck == self.parameters.get('limit_luck'):
                    self.health += self.parameters.get('gain_health_by_luck')
            else: self.health -= self.parameters.get('loss_health_by_luck')
        if self.coins > self.parameters.get('limit_coins'):
            self.honor -= self.parameters.get('loss_honor_by_coins')


class User(Player):

    def __init__(self, wire: socket, id: int, **kwargs) -> None:
        super().__init__(print, **kwargs)
        self.wire: socket = wire
        self.id: int = id
        self.controller: Lock = Lock()
        self.user_name: str = ''

    def __str__(self) -> str:
        return f'User {self.id}:{self.user_name}' if self.user_name != '' else \
        f'User {self.id}:NaN'
    
    def __repr__(self) -> str:
        return self.__str__()
    

class Card:
    health: int = 0
    honor: int = 0
    luck: int = 0
    coins: int = 0



class Deck:

    @staticmethod
    def draw() -> Card:
        new_carta = Card()
        element1 = rint(1, 4)
        val1 = rint(-3, 3)
        match element1:
            case 1: new_carta.vida = val1
            case 2: new_carta.honor = val1
            case 3: new_carta.suerte = val1
            case 4: new_carta.dinero = val1
        
        element2 = rint(1, 4)
        while element1 == element2: element2 = rint(1, 4)
        if val1 > 0: val2 = rint(-3, 0)
        elif val1 <= 0: val2 = rint(0, 3)
        match element2:
            case 1: new_carta.vida = val2
            case 2: new_carta.honor = val2
            case 3: new_carta.suerte = val2
            case 4: new_carta.dinero = val2
        return new_carta