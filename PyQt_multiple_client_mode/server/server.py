from entities import User
from itertools import count
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from net_logics import Router, Cmd
from waiting_room import WaitingRoom
from game import Game
import json


class Server:

    server_socket = socket(AF_INET, SOCK_STREAM)
    _user_counter = count(start=1)
    _games_counter = count(start=1)
    connected_users: dict[int, User] = {}
    active_games: dict[int, Game]= {}
    with open('parameters.json', mode='r', encoding='utf-8') as raw:
        parameters = json.load(raw)

    def __init__(self, host: str, port: int) -> None:
        print('Initializing Server...')
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f'Listening at {host}:{port}')
        self.waiting_room = WaitingRoom(self.launch_new_game)
        self.start_connections_thread()

    """
    NETWORKING
    """
    def start_connections_thread(self) -> None:
        print('Starting connections thread...')
        thread = Thread(target=self.accept_connections)
        thread.start()
        print('Connections thread started')

    def accept_connections(self) -> None:
        print('Server accepting connections.')
        try:    
            while True:
                client_wire, (client_addrs, client_port) = self.server_socket.accept()
                new_user = User(client_wire, next(self._user_counter),
                                parameters=self.parameters.get('player_stats'))
                self.connected_users[new_user.id] = new_user
                listener = Thread(target=self.client_listen_login,
                                args=[new_user], daemon=True)
                listener.start()
                print(f'Connected to new user at {client_addrs}:{client_port}')
        except OSError:
            print("Server was closed. Can't accept new clients")

    def client_listen_login(self, user: User) -> None:
        try:
            request = Router.receive_request(user)
            self.read_login(request, user)
        except ConnectionError:
            # handle disconnection
            pass

    """
    REQUESTS
    """
    def read_login(self, request: dict, user: User) -> None:
        username_requested = request.get('name')
        print(f'{user} requests for name {username_requested}')
        
        # if name is not available, reject and start a new listener
        errors = self.available_user_name(username_requested)
        if errors:
            Router.starken(Cmd.user_name_check(errors), user)
            listener = Thread(target=self.client_listen_login,
                              args=[user], daemon=True)
            listener.start()
            print(f'User name {username_requested} was rejected')
            return
        
        # if there are no errors with the name, the user enters the waiting room
        print(f'Username {username_requested} was accepted')
        self.user_name_check(errors, user)
        user.user_name = username_requested
        self.waiting_room.joins(user)

    """
    COMMANDS
    """
    def user_name_check(self, errors: list, user: User) -> None:
        Router.starken(Cmd.user_name_check(errors), user)

    def opponent_name(self, users: tuple[User]) -> None:
        user_1, user_2 = users
        print('OPPONENT NAME FUNCTION', users)
        Router.starken(Cmd.opponent_name(user_2.user_name), user_1)
        Router.starken(Cmd.opponent_name(user_1.user_name), user_2)

    def show_game(self, users: tuple[User]) -> None:
        user_1, user_2 = users
        Router.starken(Cmd.show_game(), user_1)
        Router.starken(Cmd.show_game(), user_2)

    """
    TASKS
    """
    def available_user_name(self, user_name: str) -> list:
        errors: list = list()
        if not user_name: errors.append('void')
        for each in self.connected_users.values():
            if user_name == each.user_name:
                errors.append('existing')
                break
        return errors
    
    # This is called from the WaitingRoom
    def launch_new_game(self, players: tuple[User]) -> None:
        # inform the users to enter a game
        self.opponent_name(players)
        self.show_game(players)
        # create a new game
        new_game = Game(players, next(self._games_counter))
        self.active_games[new_game.id] = new_game
        new_game.start() # might be deleted
        pass