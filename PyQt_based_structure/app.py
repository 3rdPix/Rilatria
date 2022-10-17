from PyQt5.QtWidgets import QApplication

from ft.win_structure import GameWindow


class Rilatria(QApplication):

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        # Instance the window
        self.window: GameWindow = GameWindow()
        self.window.show()