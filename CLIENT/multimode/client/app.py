from PyQt5.QtWidgets import QApplication

from ft.gamewin import GameWindow
from ft.welcome_window import WelWin

from bk.gamewin import GameWinLog


class Rilatria(QApplication):

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        # Instance the window front
        self.gamewin_ft: GameWindow = GameWindow()
        self.welwin_ft: WelWin = WelWin()

        # Instance the window back
        self.gamewin_bk: GameWinLog = GameWinLog()

        
        self.connect_signals()

        self.gamewin_ft.show()

    def connect_signals(self) -> None:
        
        self.welwin_ft.sg_play.connect(
            self.gamewin_bk.receive_start)
        
        self.gamewin_bk.sg_starting_data.connect(
            self.gamewin_ft.init_gui)
