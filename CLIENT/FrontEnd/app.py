#IMPORT MODULES
from FrontEnd.win_structure import GameWindow #Cambiar porque se une FE con BE

#IMPORT PYQT5
from PyQt5.QtWidgets import QApplication


class Rilatria(QApplication):

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        # Instance the window
        self.window: GameWindow = GameWindow()
        self.window.show()