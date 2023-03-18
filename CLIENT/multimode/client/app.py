from PyQt5.QtWidgets import QApplication

from ft.gamewin import GameWindow
from ft.welcome_window import WelWin

from bk.game_logic import ClientLogic


class Rilatria(QApplication):

    def __init__(self, argv: list[str], host: str, port: int) -> None:
        super().__init__(argv)

        # Instance front
        self.ft_game: GameWindow = GameWindow()
        self.ft_login: WelWin = WelWin()

        # Instance back
        self.t_client: ClientLogic = ClientLogic(host, port)

        
        self.connect_signals()
        self.t_client.launch()



    def connect_signals(self) -> None:
        
        self.t_client.ant_show_login.connect(
            self.ft_login.show)
        
        self.ft_login.ant_request_login.connect(
            self.t_client.request_login)
        
        self.t_client.ant_wire_error.connect(
            self.ft_login.mostrar_conx_err)
        
        self.t_client.ant_login_error.connect(
            self.ft_login.mostrar_name_err)
        pass
