from entities import User, Deck, Card
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
        self.player_1: User = players[0]
        self.player_2: User = players[1]
        self.players: dict[str, User] = {
            self.player_1.user_name : self.player_1,
            self.player_2.user_name : self.player_2}
        self._current_card_options: list[Card] = list()

    """
    PROPERTIES
    """


    """
    NETWORKING
    """

    def set_linsteners(self) -> None:
        listener_1 = Thread(target=self.client_listen_thread,
                            name=self.player_1.user_name,
                            args=[self.player_1], daemon=True)
        listener_2 = Thread(target=self.client_listen_thread,
                            name=self.player_2.user_name,
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
        key = request.get('request')
        match key:
            case 'finish_turn': self.finish_turn()
        pass

    def finish_turn(self) -> None:
        asker: str = current_thread().name
        self.controller.acquire()
        if not self.players[asker].my_turn: return
        self.player_1.my_turn = not self.player_1.my_turn
        self.player_2.my_turn = not self.player_2.my_turn
        self.controller.release()
        self.turn_change()
        pass

    """
    COMMANDS
    """
    def turn_change(self) -> None:
        cmd = Cmd.turn_change()
        Router.starken(cmd, self.player_1)
        Router.starken(cmd, self.player_2)

    def update_stats(self) -> None:
        # Sends the information with stats of/for both players

        # p1 -> p1
        Router.starken(Cmd.stat_update('health', self.player_1.health, True), self.player_1)
        Router.starken(Cmd.stat_update('honor', self.player_1.honor, True), self.player_1)
        Router.starken(Cmd.stat_update('luck', self.player_1.luck, True), self.player_1)
        Router.starken(Cmd.stat_update('coins', self.player_1.coins, True), self.player_1)

        # p1 -> p2
        Router.starken(Cmd.stat_update('health', self.player_1.health, False), self.player_2)
        Router.starken(Cmd.stat_update('honor', self.player_1.honor, False), self.player_2)
        Router.starken(Cmd.stat_update('luck', self.player_1.luck, False), self.player_2)
        Router.starken(Cmd.stat_update('coins', self.player_1.coins, False), self.player_2)

        # p2 -> p2
        Router.starken(Cmd.stat_update('health', self.player_2.health, True), self.player_2)
        Router.starken(Cmd.stat_update('honor', self.player_2.honor, True), self.player_2)
        Router.starken(Cmd.stat_update('luck', self.player_2.luck, True), self.player_2)
        Router.starken(Cmd.stat_update('coins', self.player_2.coins,  True), self.player_2)

        # p2 -> p1
        Router.starken(Cmd.stat_update('health', self.player_2.health, False), self.player_1)
        Router.starken(Cmd.stat_update('honor', self.player_2.honor, False), self.player_1)
        Router.starken(Cmd.stat_update('luck', self.player_2.luck, False), self.player_1)
        Router.starken(Cmd.stat_update('coins', self.player_2.coins, False), self.player_1)

    def show_cards(self) -> None:
        sendable = list()
        for each in self._current_card_options:
            option = {
                'health': each.health,
                'honor': each.honor,
                'luck': each.luck,
                'coins': each.coins
            }
            sendable.append(option)
        Router.starken(Cmd.show_cards(sendable), self.player_1)
        Router.starken(Cmd.show_cards(sendable), self.player_2)
        
    """
    TASKS
    """
    def start(self) -> None:
        # Inform the initial stats
        self.update_stats()

        # Player 1 starts the game
        self.player_1.my_turn = not self.player_1.my_turn
        Router.starken(Cmd.turn_change(), self.player_1)
        self.set_linsteners()

    def reserva_stage(self) -> None:
        if 

    def cards_stage(self) -> dict:
        self._current_card_options = list()
        for _ in range(3):
            self._current_card_options.append(Deck.draw())
        self.show_cards()