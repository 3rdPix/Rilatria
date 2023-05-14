from PyQt5.QtCore import QObject, pyqtSignal, QThread
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
            case 'stat_update': self.receive_stat_update(cmd)
            case 'show_cards': self.receive_cards(cmd)
            case 'update_board': self.update_board(cmd)

    def starken(self, object) -> None:
        if not self.connected: return
        msg = Router.codificar_bytes(object)
        self.t_socket.sendall(msg)


    """
    INSTRUCTIONS
    """
    def receive_stat_update(self, details: dict) -> None:
        self.ant_update_stat.emit(details)

    def receive_cards(self, cmd: dict) -> None:
        cards = cmd.get('cards')
        options = list()
        for card in cards:
            first = list()
            if card['health'] != 0: first.append(('health', card['health']))
            if card['honor'] != 0: first.append(('honor', card['honor']))
            if card['luck'] != 0: first.append(('luck', card['luck']))
            if card['coins'] != 0: first.append(('coins', card['coins']))
            while len(first) < 2:
                first.append(('placeholder', '0'))
            options.extend(first)
        self.ant_card_options.emit(options)

    """
    Login
    """
    def request_login(self, user: str) -> None:
        if not self.connected: self.create_connection()
        self.starken(Requests.user_name(user))
        self.username = user

    def receive_login(self, instruction) -> None:
        if not instruction.get('valid'):
            self.ant_login_error.emit(instruction.get('errors'))
            return
        self.ant_go_waiting.emit(self.username)
        self.ant_me_name.emit(self.username)
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

    def update_board(self, cmd: dict) -> None:
        self.ant_update_board.emit(cmd.get('board'))

    def change_turn(self) -> None:
        self.my_turn = not self.my_turn
        self.ant_my_turn.emit(self.my_turn)

    def card_picked(self, option: int) -> None:
        self.starken(Requests.pick_card(option))

    def cell_clicked(self, cell: tuple) -> None:
        self.starken(Requests.cell_clicked(cell))