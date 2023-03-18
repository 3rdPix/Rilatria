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
            client_socket, (client_addrs, client_port) = self.sv_socket.accept()
            self.log(1, f'Connected to new client at {client_addrs}:{client_port}')
            player = Player(ip=client_addrs, wing=client_socket)
            self.players[client_socket] = player
            listener = threading.Thread(
                target=self.client_listen_thread,
                args=(client_socket, ),
                daemon=True)
            listener.start()

    def client_listen_thread(self, client_socket: socket) -> None:
        try:
            while True:
                len_in_bytes = client_socket.recv(4)
                content_length = int.from_bytes(
                    len_in_bytes, byteorder='big')
                request = Router.recibir_bytes(
                    content_length, client_socket)
                self.read_request(request, client_socket)
        except ConnectionError:
            self.handle_disconnection(client_socket)

    def handle_disconnection(self, client: socket) -> None:
        gone = self.players.get(client)
        self.log(1, f'Sudden disconnection at {gone.ip}')
        if self.lobby.exists(gone):
            self.lobby.leaves(gone)
            if not self.lobby.is_Empty():
                self.starken(Instructions.avisar_abandono_espera(),
                    self.lobby.j1.wing)
        del self.players[client]
        del client
            
    def read_request(self, request: dict, wire: socket) -> None:
        match request.get('request'):
            case 'user_name': self.ver_usuario(request, wire)

    def starken(self, objeto, wing: socket) -> None:
        msg = Router.codificar_bytes(objeto)
        traffic_handler: threading.Lock = self.players.get(wing).controller
        traffic_handler.acquire()
        wing.sendall(msg)
        traffic_handler.release()

    def ver_usuario(self, request: dict, wire: socket) -> None:
        nick: str = request.get('name')
        self.log(2, f'User at {self.players.get(wire).ip} request for name "{nick}"')
        errors: list = list()
        if nick == '': errors.append('void')
        for jugador in self.players.values():
            if jugador.username == nick:
                errors.append('existing')
                break
        errors.append('existing')
        if errors:
            self.log(1, f'Username {nick} has been rejected')
            self.starken(Instructions.user_name_check(errors), wire)
        else:
            self.log(1, f'Username {nick} has been accepted')
            self.players.get(wire).username = nick
            self.starken(Instructions.user_name_check(errors), wire)
            self.lobby.joins(self.players.get(wire))
            if self.lobby.is_Full(): self.atender_sala_espera()

    def atender_sala_espera(self) -> None:
        order_1 = Instructions.info_adv(self.lobby.j2.username)
        order_2 = Instructions.info_adv(self.lobby.j1.username)
        self.starken(order_1, self.lobby.j1.wing)
        self.starken(order_2, self.lobby.j2.wing)
        self.lobby.empieza_conteo()
