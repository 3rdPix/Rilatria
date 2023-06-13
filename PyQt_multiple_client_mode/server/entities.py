from socket import socket
from threading import Lock
from random import randint as rint
from abc import ABC

class Card:
    health: int = 0
    honor: int = 0
    luck: int = 0
    coins: int = 0



class Deck:

    @staticmethod
    def draw() -> Card:
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
        self._moved_hero: bool = False
        self._moved_piece: bool = False
        self._is_moving: bool = False

    """
    PUBLIC
    """
    def is_alive(self) -> bool:
        if self.health < 1: return False
        if self.coins < 1 and self.luck < 1: return False
        return True
    
    def apply_card(self, card: Card) -> None:
        self.health += card.health
        self.honor += card.honor
        self.luck += card.luck
        self.coins += card.coins
    
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
    

class Piece(ABC):

    def __init__(self, belongs_to: int, parameters: dict) -> None:
        super().__init__()
        self.owner: int = belongs_to
        self.legal_moves: list = parameters.get('moves')
        self.legal_eats: list = parameters.get('eats')

class Barbarian(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'Barbarian'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class HorseRider(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'Horserider'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class Spearman(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'Spearman'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class RattleTrap(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'RattleTrap'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class Joker(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'Joker'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class Hero(Piece):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = 'Hero'

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

class Cell:

    def __init__(self) -> None:
        self.contains: Piece|None = None

    def place_piece(self, piece: Piece) -> None:
        self.contains = piece

    def is_occupied(self) -> bool:
        return True if self.contains else False

    def __str__(self) -> str:
        if self.contains:
            return self.contains.__str__()
        else:
            return f"X"

class Board:

    def __init__(self, board_parameters: dict, piece_parameters: dict,
                 p1: User, p2: User) -> None:
        self.cells: list[list[Cell]] = [
            [Cell() for _ in range(9)] for _ in range(9)]
        self.init_piece: dict[str, Piece] = {
            'Barbarian': Barbarian,
            'Horserider': HorseRider,
            'Spearman': Spearman,
            'RattleTrap': RattleTrap,
            'Joker': Joker,
            'Hero': Hero}
        self.parameters: dict = board_parameters
        self.piece_parameters: dict = piece_parameters
        self.owners: dict[int, User] = {1: p1, 2: p2}
        self.selected_piece: tuple[int]|None = None
        self.set_prices(piece_parameters)
        self.set_starting_pieces()

    def set_starting_pieces(self) -> None:
        pieces = self.parameters.get('starting_pieces')
        for each in pieces:
            y, x, piece, owner = each
            self.cells[y][x].place_piece(
                self.init_piece[piece](
                belongs_to=self.owners[owner],
                parameters=self.piece_parameters[piece]))

    def set_prices(self, piece_parameters: dict) -> None:
        self.prices: dict[str, int] = {
            'Barbarian': piece_parameters.get('Barbarian').get('price'),
            'Horserider': piece_parameters.get('Horserider').get('price'),
            'Spearman': piece_parameters.get('Spearman').get('price'),
            'RattleTrap': piece_parameters.get('RattleTrap').get('price'),
            'Joker': piece_parameters.get('Joker').get('price')}

    def is_cell_occupied(self, x: int, y: int) -> bool:
        return self.cells[y][x].is_occupied()
        
    def get_sendable(self) -> list:
        sendable_board = list()
        for row in self.cells:
            sendable_row = list()
            for cell in row:
                if cell.contains: sendable_row.append(cell.contains.name)
                else: sendable_row.append('X')
            sendable_board.append(sendable_row)
        return sendable_board
    
    def is_whos(self, x: int, y: int) -> User|bool:
        if self.cells[y][x].contains:
            return self.cells[y][x].contains.owner
        else:
            return False

    def has_selected_piece(self) -> bool:
        return True if self.selected_piece else False
    
    def get_legal_moves(self, x: int, y: int, p: User) -> list:
        if not self.is_cell_occupied(x, y): return
        print('CLICKED CELL:', x, y)

        # step 1: get what cells exists in the board around selection
        neighbourhood = self.adjacent_finder(x, y, 2)
        print('NEIGHBOURHOOD:', neighbourhood)
        
        # step 2: get what cells is the piece wanting to go
        relative_moves = self.cells[y][x].contains.legal_moves
        relative_eats = self.cells[y][x].contains.legal_eats
        print('RELATIVE MOVES:', relative_moves)

        absolute_moves = self.relative_to_absolute(x, y, relative_moves)
        absolute_eats = self.relative_to_absolute(x, y, relative_eats)
        print('ABSOLUTE MOVES', absolute_moves)
        
        # step 3: cross this information
        valid_moves = self.find_common(neighbourhood, absolute_moves)
        valid_eats = self.find_common(neighbourhood, absolute_eats)
        print('VALID MOVES', valid_moves)

        # step 4: verify if target moving cells are available
        legal_moves = self.find_free_cells(valid_moves)
        legal_eats = self.find_legal_eats(valid_eats, p)
        print('LEGAL MOVES', legal_moves)

        return legal_moves, legal_eats

    def find_free_cells(self, options: list) -> list:
        free_cells = list()
        for target in options:
            x, y = target
            if not self.is_cell_occupied(x, y): free_cells.append(target)
        return free_cells

    def find_legal_eats(self, options: list, p: User) -> list:
        occupied_cells = list()
        for target in options:
            x, y = target
            if not self.is_cell_occupied(x, y): continue
            owner = self.cells[y][x].contains.owner
            if not owner is p: occupied_cells.append(target)
        return occupied_cells

    def find_common(self, king: list, *args) -> list:
        common = list()
        for collection in args:
            for option in collection:
                if option in king: common.append(option)
        return common

    def relative_to_absolute(self, x: int, y: int, rel: list) -> list:
        absolute = list()
        for target in rel:
            i, j = target
            absolute.append([x + i, y + j])
        return absolute

    def adjacent_finder(self, i: int, j: int, md: int) -> list:
            neighbour = []
            for dx in range(-md, md + 1):
                for dy in range(-md, md + 1):
                    rangeX = range(0, 9)
                    rangeY = range(0, 9)
                    (newX, newY) = (i + dx, j + dy)
                    if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
                        neighbour.append([newX, newY])
            return neighbour

    def try_legal_move(self, x: int, y: int) -> bool:
        pass

    def __str__(self) -> str:
        for row in self.cells:
            print(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7], row[8])
        return ''