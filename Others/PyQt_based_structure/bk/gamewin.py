from PyQt5.QtCore import QObject, pyqtSignal


class GameWinLog(QObject):

    sg_starting_data = pyqtSignal(tuple)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def receive_start(self, data: tuple) -> None:
        self.sg_starting_data.emit(data)