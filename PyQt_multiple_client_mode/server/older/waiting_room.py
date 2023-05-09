from threading import Thread, Lock
from itertools import count
from entities import User
from time import sleep
from net_logics import Router, Cmd
from PyQt5.QtCore import pyqtSignal


class Node:

    def __init__(self, value: User=None):
        self.value: User|None = value
        self.next: User|None= None


class WaitingRoomQueue:

    controller = Lock()

    def __init__(self):
        self.first = None
        self.last = None
        
    def add(self, value: User):
        new = Node(value)
        self.controller.acquire()
        if self.first is None:
            self.first = new
            self.last = self.first
        else:
            self.last.next = new
            self.last = self.last.next
        self.controller.release()
        print(self)
    
    def call_next(self) -> User|None:
        self.controller.acquire()
        if not self.first:
            self.controller.release()
            return None
        old_first = self.first
        new_first = self.first.next
        self.first = new_first
        give = old_first.value
        del old_first
        self.controller.release()
        return give
    
    # someday will use this to avoid permarunning of game launches
    def get_length(self) -> None:
        counter: int = 1
        counting_who: Node = self.first
        while not counting_who is self.last:
            counter += 1
            counting_who = counting_who.next
        return counter
    
    def call_two(self) -> tuple[User]|None:
        print('Queue: getting the two')
        self.controller.acquire()
        
        # not enough players
        if not self.first or not self.first.next:
            self.controller.release()
            return None
        
        # if enough players
        old_first = self.first
        new_first = self.first.next
        self.first = new_first
        p1 = old_first.value

        old_first2 = self.first
        new_first2 = self.first.next
        self.first = new_first2
        p2 = old_first2.value
        self.controller.release()
        del old_first
        del old_first2
        print(self)
        return (p1, p2)
    
    def leaves(self, value: User) -> None:
        self.controller.acquire()
        checking_on: Node = self.first
        if checking_on.value == value:
            new_first: Node = self.first.next
            del self.first
            self.first: Node = new_first
            self.controller.release()
            return
        while checking_on.value != value:
            next_to_check: Node = checking_on.next
            if value == next_to_check.value:
                new_next: Node = next_to_check.next
                checking_on.next = new_next
                del next_to_check
                self.controller.release()
                return
            if not next_to_check:
                self.controller.release()
                return

    def __repr__(self):
        self.controller.acquire()
        
        # no one here
        if not self.first:
            self.controller.release()
            return "-----\nEmpty\n-----"
        
        # if there are players
        string = "-----\n"
        current = self.first
        while current is not None:
            string = f"{string}{current.value} → "
            current = current.next
        self.controller.release()
        return string + "\n-----"

class WaitingRoom:

    queue = WaitingRoomQueue()
    controller = Lock()

    def __init__(self, count_start: int, observer) -> None:
        super().__init__()
        self.observer = observer
        self.present_players: list[User] = list()

    def joins(self, player: User) -> None:
        self.queue.add(player)
        self.controller.acquire()
        self.present_players.append(player)
        self.controller.release()
        self.launch_with_two()

    def leaves(self, player: User) -> None:
        self.controller.acquire()
        self.queue.leaves(player)
        self.present_players.remove(player)
        self.controller.release()

    def launch_with_two(self) -> None:
        print('Trying to launch with two')
        players = self.queue.call_two()
        if not players:
            print('not enough players')
            return
        self.controller.acquire()
        self.present_players.remove(players[0])
        self.present_players.remove(players[1])
        self.controller.release()
        print(players)
        return self.observer(players)
        print('observer called')


    def __repr__(self) -> str:
        return self.queue.__repr__()