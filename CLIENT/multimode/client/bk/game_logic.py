from PyQt5.QtCore import QObject, pyqtSignal, QThread
from bk.entities import Player, Board, Piece, Deck
from bk.logics import Router, Requests
from bk.game_sg import Signals
from socket import socket as wire, AF_INET, SOCK_STREAM
from threading import Thread


class ClientLogic(Signals):

    def __init__(self, host: str, port: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.my_turn: bool = False

    def launch(self) -> None:
        self.ant_show_login.emit()
        self.connected = False

    """
    Connection
    """

    def create_connection(self) -> None:
        self.t_socket: wire = wire(AF_INET, SOCK_STREAM)
        try:
            self.t_socket.connect((self.host, self.port))
            self.connected = True
            self.reception_thread()
        except ConnectionError as e:
            self.ant_wire_error.emit(e)
            self.connected = False

    def reception_thread(self) -> None:
        thread = Thread(target=self.listen_server, daemon=True)
        thread.start()

    def listen_server(self) -> None:
        while self.connected:
            try:
                len_in_bytes = self.t_socket.recv(4)
                content_length = int.from_bytes(len_in_bytes, byteorder='big')
                instructions = Router.recibir_bytes(content_length, self.t_socket)
                self.read_instruction(instructions)
            except ConnectionAbortedError: break

    def read_instruction(self, cmd) -> None:
        match cmd.get('cmd'):
            case 'user_name_check': self.receive_login(cmd)
            case 'opponent_name': self.receive_opponent_name(cmd)
            case 'show_game': self.show_game()
            case 'turn_change': self.change_turn()

    def starken(self, object) -> None:
        if not self.connected: return
        msg = Router.codificar_bytes(object)
        self.t_socket.sendall(msg)

    """
    Login
    """
    def request_login(self, user: str) -> None:
        if not self.connected: self.create_connection()
        print(user)
        self.starken(Requests.user_name(user))
        self.username = user

    def receive_login(self, instruction) -> None:
        if not instruction.get('valid'):
            self.ant_login_error.emit(instruction.get('errors'))
            return
        print('1')
        self.ant_go_waiting.emit(self.username)
        print('2')
        self.ant_me_name.emit(self.username)
        print('3')
        pass

    def request_finish_turn(self) -> None:
        self.starken(Requests.finish_turn())

    """
    Game
    """
    def receive_opponent_name(self, cmd: dict) -> None:
        self.ant_opponent_name.emit(cmd.get('name'))

    def show_game(self) -> None:
        self.ant_show_game.emit()

    def change_turn(self) -> None:
        self.my_turn = not self.my_turn
        self.ant_my_turn.emit(self.my_turn)