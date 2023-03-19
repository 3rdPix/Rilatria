from socket import socket, AF_INET, SOCK_STREAM
from logicas import Router, Instructions
from sala_espera import WaitingRoom
from entidades import Player
import threading
from json import load

class Server:


    def __init__(self, port: int, host: str) -> None:
        print("Initializing Server...")
        self.host = host
        self.port = port
        self.sv_socket: socket = socket(AF_INET, SOCK_STREAM)
        self.players: dict[socket, Player] = dict()
        self.lobby: WaitingRoom = WaitingRoom(
            count_start=10,
            router=Router(), instructions=Instructions())
        self.bind_and_listen()
        self.start_connections_thread()

    def log(self, format: int, msg: str) -> None:
        match format:
            case 0: print('[STATUS]', msg)
            case 1: print('[EVENT]', msg)
            case 2: print('[REQUEST]', msg)

    """
    Network
    """
    def bind_and_listen(self) -> None:
        self.sv_socket.bind((self.host, self.port))
        self.sv_socket.listen()
        self.log(0, f'Server listening at {self.host}:{self.port}...')

    def start_connections_thread(self) -> None:
        self.log(1, 'Starting connections thread...')
        thread = threading.Thread(target=self.accept_connections)
        thread.start()
        self.log(0, 'Connections thread started.')

    def accept_connections(self) -> None:
        self.log(0, 'Server accepting connections...')
        while True:
            end_wire, (end_addrs, end_port) = self.sv_socket.accept()
            self.log(1, f'Connected to new client at {end_addrs}:{end_port}')
            self.players[end_wire] = Player(ip=end_addrs, wire=end_wire)
            listener = threading.Thread(
                target=self.end_listen_thread,
                args=(end_wire, ),
                daemon=True)
            listener.start()

    def end_listen_thread(self, end_wire: socket) -> None:
        try:
            while True:
                len_in_bytes = end_wire.recv(4)
                content_length = int.from_bytes(
                    len_in_bytes, byteorder='big')
                request = Router.recibir_bytes(
                    content_length, end_wire)
                self.read_request(request, end_wire)
        except ConnectionError:
            self.handle_disconnection(end_wire)

    def handle_disconnection(self, end_wire: socket) -> None:
        gone: Player = self.players.get(end_wire)
        self.log(1, f'Sudden disconnection at {gone.ip}')
        if self.lobby.exists(gone):
            self.lobby.leaves(gone)
        del self.players[end_wire]
        del end_wire

    def starken(self, objeto, end_wire: socket) -> None:
        msg = Router.codificar_bytes(objeto)
        traffic_handler: threading.Lock = self.players.get(end_wire).controller
        traffic_handler.acquire()
        end_wire.sendall(msg)
        traffic_handler.release()
    
    """
    Requests
    """
    def read_request(self, request: dict, end_wire: socket) -> None:
        match request.get('request'):
            case 'user_name': self.ver_usuario(request, end_wire)

    def ver_usuario(self, request: dict, end_wire: socket) -> None:
        nick: str = request.get('name')
        self.log(2, f'User at {self.players.get(end_wire).ip} requests for name "{nick}"')
        
        # search for errors
        errors: list = list()
        if not nick: errors.append('void')
        for jugador in self.players.values():
            if jugador.username == nick:
                errors.append('existing')
                break
        
        # resolve errors
        if errors:
            self.log(1, f'Username {nick} has been rejected')
            self.starken(Instructions.user_name_check(errors), end_wire)
        else:
            # inform of success
            self.log(1, f'Username {nick} has been accepted')
            self.players.get(end_wire).username = nick
            self.starken(Instructions.user_name_check(errors), end_wire)

            # handle new player
            self.lobby.joins(self.players.get(end_wire))

    """
    Instructions
    """

    def atender_sala_espera(self) -> None:
        order_1 = Instructions.info_adv(self.lobby.j2.username)
        order_2 = Instructions.info_adv(self.lobby.j1.username)
        self.starken(order_1, self.lobby.j1.wire)
        self.starken(order_2, self.lobby.j2.wire)
        self.lobby.empieza_conteo()

    """
    Tasks
    """
