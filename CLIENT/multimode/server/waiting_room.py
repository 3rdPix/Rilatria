from threading import Thread
from itertools import count
from entities import Player
from time import sleep
from logics import Router, Instructions


class Node:

    def __init__(self, value: Player=None):
        self.value: Player|None = value
        self.next: Player|None= None


class WaitingRoomQueue:

    def __init__(self):
        self.first = None
        self.last = None
        
    def add(self, value: Player):
        new = Node(value)
        if self.first is None:
            self.first = new
            self.last = self.first
        else:
            self.last.next = new
            self.last = self.last.next
    
    def call_next(self) -> Player|None:
        if not self.first: return None
        old_first = self.first
        new_first = self.first.next
        self.first = new_first
        give = old_first.value
        del old_first
        return give
    
    def leaves(self, value: Player) -> None:
        checking_on: Node = self.first
        if checking_on.value == value:
            new_first: Node = self.first.next
            del self.first
            self.first: Node = new_first
            return
        while checking_on.value != value:
            next_to_check: Node = checking_on.next
            if value == next_to_check.value:
                new_next: Node = next_to_check.next
                checking_on.next = new_next
                del next_to_check
                return
            if not next_to_check: return

    def __repr__(self):
        if not self.first: return "Vacía"
        string = ""
        current = self.first
        while current is not None:
            string = f"{string}{current.value} → "
            current = current.next
        return string


class WaitingRoom:

    time_counter: count
    remaining_time: int = 10
    queue = WaitingRoomQueue()

    def __init__(self, count_start: int) -> None:
        self.j1: Player = None
        self.j2: Player = None
        self.counting = False
        self.starts_in = count_start
        self.time_counter = count(start=self.starts_in, step=-1)
        self.present_players: list[Player] = list()

    def joins(self, player: Player) -> None:
        if self.is_Full(): self.queue.add(player)
        if not self.j1: self.j1 = player
        elif not self.j2: self.j2 = player
        self.present_players.append(player)
        print(self)

    def is_Full(self) -> bool:
        if self.j1 and self.j2: return True
        return False

    def is_Empty(self) -> bool:
        if self.j1 or self.j2: return False
        return True

    def clear(self) -> None:
        self.j1 = None
        self.j2 = None

    def leaves(self, player: Player) -> None:
        if player is self.j1:
            self.cancel_counting()
            self.j1 = self.j2
            self.j2 = self.queue.call_next()
        elif player is self.j2:
            self.cancel_counting()
            self.j2 = self.queue.call_next()
        else:
            self.queue.leaves(player)
        self.present_players.remove(player)
        print(self)

    def start_counting(self) -> None:
        self.counting_thread = Thread(target=self.count_time, daemon=True)
        self.counting = True
        self.counting_thread.start()

    def count_time(self) -> None:
        while self.remaining_time > 0:
            if not self.counting: return
            self.remaining_time = next(self.time_counter)
            self.starken_time(self.remaining_time)
            sleep(1)
        
    def cancel_counting(self) -> None:
        self.counting = False
        self.remaining_time = 10
        self.time_counter = count(start=self.starts_in, step=-1)

    def is_Counting(self) -> bool:
        return self.counting
        
    def exists(self, player: Player) -> bool:
        return player in self.present_players

    def starken_time(self, time: int) -> None:
        tiempo = Instructions.remaining_time(time)
        msg = Router.code_bytes(tiempo)
        self.j1.controller.acquire()
        self.j1.wire.sendall(msg)
        self.j1.controller.release()
        self.j2.controller.acquire()
        self.j2.wire.sendall(msg)
        self.j2.controller.release()

    def __repr__(self) -> str:
        if self.is_Full():
            screen: str = f'''[STATE]
    -- Lobby --
     Player 1: {self.j1.username}, at {self.j1.ip}
     Player 2: {self.j2.username}, at {self.j2.ip}
    --------------------
    -- Queue --
    {self.queue}
    ----------
        '''
        elif self.is_Empty():
            screen: str = f'''[STATE]
    -- Lobby --
     Empty
    --------------------
    -- Queue --
    {self.queue}
    ----------
        '''
        else:
            screen: str = f'''[STATE]
    -- Lobby --
     Player 1: {self.j1.username}, at {self.j1.ip}
    --------------------
    -- Queue --
    {self.queue}
    ----------
        '''
        return screen