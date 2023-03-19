from PyQt5.QtWidgets import QApplication

from ft.gamewin import GameWindow
from ft.welcome_window import WelWin

from bk.game_logic import ClientLogic

import json


class Rilatria(QApplication):

    def __init__(self, argv: list[str], host: str, port: int) -> None:
        super().__init__(argv)

        with open('preset_app.json', 'r') as raw: preset = json.load(raw)
        self.lang = preset.get('lang')

        # Instance front
        self.ft_game: GameWindow = GameWindow(self.lang)
        self.ft_login: WelWin = WelWin(self.lang)

        # Instance back
        self.t_client: ClientLogic = ClientLogic(host, port)

        
        self.connect_signals()
        self.t_client.launch()



    def connect_signals(self) -> None:
        
        self.t_client.ant_show_login.connect(
            self.ft_login.show)
        
        self.ft_login.ant_request_login.connect(
            self.t_client.request_login)
        
        self.ft_login.ant_update_lang.connect(
            self.update_default_lang)
        
        self.t_client.ant_wire_error.connect(
            self.ft_login.connection_error_message)
        
        self.t_client.ant_login_error.connect(
            self.ft_login.username_error_message)
        pass

    def update_default_lang(self, lang: int) -> None: self.lang = lang
