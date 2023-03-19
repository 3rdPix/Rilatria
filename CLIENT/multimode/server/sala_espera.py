from socket import socket
from threading import Thread
from itertools import count
from entidades import Player
from time import sleep


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

    contador: count
    tiempo_restante: int = 10
    queue = WaitingRoomQueue()

    def __init__(self, count_start: int, router, instructions) -> None:
        self.j1: Player = None
        self.j2: Player = None
        self.contando = False
        self.inicia_en = count_start
        self.router = router
        self.cmd = instructions
        self.contador = count(start=self.inicia_en, step=-1)
        self.present_players: list[Player] = list()

    def joins(self, jugador: Player) -> None:
        if self.is_Full(): self.queue.add(jugador)
        if not self.j1: self.j1 = jugador
        elif not self.j2: self.j2 = jugador
        self.present_players.append(jugador)
        print(self)

    def is_Full(self) -> bool:
        if self.j1 and self.j2: return True
        return False

    def is_Empty(self) -> bool:
        if self.j1 or self.j2: return False
        return True

    def vaciar(self) -> None:
        self.j1 = None
        self.j2 = None

    def leaves(self, player: Player) -> None:
        if player is self.j1:
            self.cancelar_conteo()
            self.j1 = self.j2
            self.j2 = self.queue.call_next()
        elif player is self.j2:
            self.cancelar_conteo()
            self.j2 = self.queue.call_next()
        else:
            self.queue.leaves(player)
        self.present_players.remove(player)
        print(self)

    def empieza_conteo(self) -> None:
        self.conteo: Thread = Thread(target=self.cuenta, daemon=True)
        self.contando = True
        self.conteo.start()

    def cuenta(self) -> None:
        while self.tiempo_restante > 0:
            if not self.contando: return
            self.tiempo_restante = next(self.contador)
            self.starken_time(self.tiempo_restante)
            sleep(1)
        
    def cancelar_conteo(self) -> None:
        self.contando = False
        self.tiempo_restante = 10
        self.contador = count(start=self.inicia_en, step=-1)

    def esta_contando(self) -> bool:
        return self.contando
        
    def exists(self, player: Player) -> bool:
        return player in self.present_players

    def starken_time(self, time: int) -> None:
        tiempo = self.cmd.informe_tiempo(time)
        msg = self.router.codificar_bytes(tiempo)
        self.j1.controller.acquire()
        self.j1.wire.sendall(msg)
        self.j1.controller.release()
        self.j2.controller.acquire()
        self.j2.wire.sendall(msg)
        self.j2.controller.release()

    def __repr__(self) -> str:
        if self.is_Full():
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Jugador 1: {self.j1.username}, en {self.j1.ip}
     Jugador 2: {self.j2.username}, en {self.j2.ip}
    --------------------
    -- Cola --
    {self.queue}
    ----------
        '''
        elif self.is_Empty():
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Vacía
    --------------------
    -- Cola --
    {self.queue}
    ----------
        '''
        else:
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Jugador 1: {self.j1.username}, en {self.j1.ip}
    --------------------
    -- Cola --
    {self.queue}
    ----------
        '''
        return mostrar