from socket import socket
from threading import Thread
from itertools import count
from entidades import Player
from time import sleep


class WaitingRoom:

    contador: count
    tiempo_restante: int = 10

    def __init__(self, count_start: int, router, instructions) -> None:
        self.j1: Player = None
        self.j2: Player = None
        self.contando = False
        self.inicia_en = count_start
        self.router = router
        self.cmd = instructions
        self.contador = count(start=self.inicia_en, step=-1)

    def joins(self, jugador: Player) -> None:
        if self.is_Full(): raise Exception('-> Sala de espera ya está llena.')
        if not self.j1: self.j1 = jugador
        elif not self.j2: self.j2 = jugador
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

    def leaves(self, client: socket) -> None:
        if client is self.j1:
            self.j1 = self.j2
            self.j2 = None
        elif client is self.j2:
            self.j2 = None
        else: return
        print(self)
        self.cancelar_conteo()

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
        return player is self.j1 or player is self.j2

    def starken_time(self, time: int) -> None:
        tiempo = self.cmd.informe_tiempo(time)
        msg = self.router.codificar_bytes(tiempo)
        self.j1.controller.acquire()
        self.j1.wing.sendall(msg)
        self.j1.controller.release()
        self.j2.controller.acquire()
        self.j2.wing.sendall(msg)
        self.j2.controller.release()

    def __repr__(self) -> str:
        if self.is_Full():
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Jugador 1: {self.j1.username}, en {self.j1.ip}
     Jugador 2: {self.j2.username}, en {self.j2.ip}
    --------------------
        '''
        elif self.is_Empty():
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Vacía
    --------------------
        '''
        else:
            mostrar: str = f'''[STATE]
    -- Sala de espera --
     Jugador 1: {self.j1.username}, en {self.j1.ip}
    --------------------
        '''
        return mostrar