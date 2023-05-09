from entities import User, Player, Deck
from threading import Thread, Lock
from socket import socket
from net_logics import Router, Cmd


class Game:

    def __init__(self, p1: User, p2: User) -> None:
        print('New game', self, 'started')
        self.create_game_variables(p1, p2)
        self.set_listening(p1, p2)

    def create_game_variables(self, user_1, user_2) -> None:
        self.users = (user_1, user_2)
        user_1.player: Player = Player(self.player_died)
        user_2.player: Player = Player(self.player_died)
        self._turn_of = 0
        self._not_turn_of = 1
        self.stat_total_turns: int = 1 # counter
        self._in_turn_stage: int = 0 # from 0 to 3
        self._in_stageX: list[bool] = [False for _ in range(4)]
        self._board = [[0 for _ in range(9)] for _ in range(9)]
        self.game_locker: Lock = Lock()

    """
    Net functionality
    """
    def set_listening(self, p1: User, p2: User) -> None:
        print('Starting listeners threads')
        listener1 = Thread(
                target=self.client_listen_thread,
                args=(p1, ),
                daemon=True)
        listener1.start()
        listener2 = Thread(
                target=self.client_listen_thread,
                args=(p2, ),
                daemon=True)
        listener2.start()

    def client_listen_thread(self, user: User) -> None:
        try:
            while user.sv_listen:
                print('started listen thread for', user)
                len_in_bytes = user.wire.recv(4)
                content_length = int.from_bytes(
                    len_in_bytes, byteorder='big')
                request = Router.receive_bytes(
                    content_length, user.wire)
                self.read_request(request, user)
        except ConnectionError:
            self.handle_disconnection(user)

    def read_request(self, rqst, user) -> None:
        match rqst.get('request'):
            case 'finish_turn': self.do_stage0()
        pass

    def player_died(self, gamer: Player) -> None:
        pass

    def starken(self, objeto, to_user: User) -> None:
        msg = Router.code_bytes(objeto)
        traffic_handler: Lock = to_user.controller
        traffic_handler.acquire()
        to_user.wire.sendall(msg)
        traffic_handler.release()

    """
    Turn stages
    """
    def do_stage0(self) -> None:
        # non-existant stage, mimic to try
        self.starken(Cmd.turn_info(True), self.users[self._turn_of])
        self.starken(Cmd.turn_info(False), self.users[self._not_turn_of])
        hold = self._turn_of.copy()
        self._turn_of = self._not_turn_of
        self._not_turn_of = hold
        pass

    def do_stage1(self) -> None:
        # automatic effects related to Player' stats
        pass

    def do_stage2(self, turn: int) -> None:
        # phase 2, user_driven
        match self._current_turn:
            case 1:
                self.starken(Cmd.turn_info(True), self.p1.wire)
                self.starken(Cmd.turn_info(False), self.p2.wire)
            case 2:
                self.starken(Cmd.turn_info(False), self.p1.wire)
                self.starken(Cmd.turn_info(True), self.p2.wire)
        cards: tuple = Deck.draw(3)
        send_out = Cmd.cards_info(cards)
        self.starken(send_out, self.p1.wire)
        self.starken(send_out, self.p2.wire)

    def do_stage3(self) -> None:
        # Movement
        pass