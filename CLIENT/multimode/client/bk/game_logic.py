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
        match cmd.get('comando'):
            case 'user_name_check': self.receive_login(cmd)

    def starken(self, object) -> None:
        if not self.connected: return
        msg = Router.codificar_bytes(object)
        self.t_socket.sendall(msg)

    """
    Login
    """
    def request_login(self, user: str) -> None:
        if not self.connected: self.create_connection()
        if self.connected: self.starken(Requests.user_name(user))

    def receive_login(self, instruction) -> None:
        if not instruction.get('valid'):
            self.ant_login_error.emit(instruction.get('errores'))
        pass
