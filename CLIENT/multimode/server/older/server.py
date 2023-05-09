from socket import socket, AF_INET, SOCK_STREAM
from net_logics import Router, Cmd
from waiting_room import WaitingRoom
from entities import User
from game import Game
import threading

class Server:

    def __init__(self, port: int, host: str) -> None:
        super().__init__()
        print("Initializing Server...")
        self.host = host
        self.port = port
        self.sv_socket: socket = socket(AF_INET, SOCK_STREAM)
        self.players: dict[socket, User] = dict()
        self.lobby = WaitingRoom(count_start=15, observer=self.start_game)
        self.active_games: list[Game] = list()
        
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
            self.players[end_wire] = User(ip=end_addrs, wire=end_wire)
            listener = threading.Thread(
                target=self.client_listen_thread,
                args=(end_wire, ),
                daemon=True)
            listener.start()

    def client_listen_thread(self, client_wire: socket) -> None:
        try:
            while self.players[client_wire].sv_listen:
                print('pre-solicitud')
                len_in_bytes = client_wire.recv(4)
                content_length = int.from_bytes(
                    len_in_bytes, byteorder='big')
                request = Router.receive_bytes(
                    content_length, client_wire)
                self.read_request(request, client_wire)
                print('solicitud')
        except ConnectionError:
            self.handle_disconnection(client_wire)

    def handle_disconnection(self, client_wire: socket) -> None:
        gone: User = self.players.get(client_wire)
        self.log(1, f'Sudden disconnection at {gone.ip}')
        self.lobby.leaves(gone)
        del self.players[client_wire]
        del client_wire

    def starken(self, objeto, client_wire: socket) -> None:
        msg = Router.code_bytes(objeto)
        traffic_handler: threading.Lock = self.players.get(client_wire).controller
        traffic_handler.acquire()
        client_wire.sendall(msg)
        traffic_handler.release()
    
    """
    Requests
    """
    def read_request(self, request: dict, client_wire: socket) -> None:
        match request.get('request'):
            case 'user_name': self.check_username(request, client_wire)
            case 'finish_turn': print('trying to finish through server')

    

    """
    Instructions
    """

    def user_name_check(self, errors: list, client_wire: socket) -> None:
        self.starken(Cmd.user_name_check(errors), client_wire)

    def opponent_name(self, users: tuple[User]) -> None:
        user_1, user_2 = users
        self.starken(Cmd.opponent_name(user_2.username), user_1.wire)
        self.starken(Cmd.opponent_name(user_1.username), user_2.wire)

    def show_game(self, users: tuple[User]) -> None:
        user_1, user_2 = users
        self.starken(Cmd.show_game(), user_1.wire)
        self.starken(Cmd.show_game(), user_2.wire)

    """
    Tasks
    """
    # this function is called from WaitingRoom
    def start_game(self, users: tuple[User]) -> None:
        # inform the users to enter a game
        self.opponent_name(users)
        self.show_game(users)
        # enter the game and rely the task of listening to the Game object
        users[0].sv_listen = False
        users[1].sv_listen = False
        new_game = Game(*users)
        self.active_games.append(new_game)

    def check_username(self, request: dict, client_wire: socket) -> None:
        nick: str = request.get('name')
        self.log(2, f'User at {self.players.get(client_wire).ip} requests for name "{nick}"')
        
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

        else:
            # handle new player
            self.log(1, f'Username {nick} has been accepted')
            self.players.get(client_wire).username = nick
        
        # inform the user
        self.user_name_check(errors, client_wire)
        self.lobby.joins(self.players.get(client_wire))