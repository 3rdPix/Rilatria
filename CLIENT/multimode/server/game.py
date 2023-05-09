from entities import User
from threading import Thread, Lock, current_thread
from socket import socket
from net_logics import Router, Cmd


class Game:

    controller = Lock()

    def __init__(self, players: tuple[User], id: int) -> None:
        print(f'Starting game with {players}')
        self.id = id
        self.create_game_variables(players)

    def create_game_variables(self, players: tuple[User]) -> None:
        self.player_1 = players[0]
        self.player_2 = players[1]

    """
    NETWORKING
    """

    def set_linsteners(self) -> None:
        listener_1 = Thread(target=self.client_listen_thread, name=self.player_1.user_name,
                            args=[self.player_1], daemon=True)
        listener_2 = Thread(target=self.client_listen_thread, name=self.player_2.user_name,
                            args=[self.player_2], daemon=True)
        listener_1.start()
        listener_2.start()

    def client_listen_thread(self, user: User) -> None:
        try:
            while True:
                request = Router.receive_request(user)
                self.read_request(request)
        except ConnectionError:
            # handle disconnection
            pass

    """
    REQUESTS
    """
    def read_request(self, request: dict) -> None:
        pass

    """
    COMMANDS
    """

    """
    TASKS
    """
    