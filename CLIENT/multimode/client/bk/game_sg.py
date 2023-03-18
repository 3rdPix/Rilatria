from PyQt5.QtCore import QObject, pyqtSignal


class Signals(QObject):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    ant_show_login = pyqtSignal()
    ant_wire_error = pyqtSignal(Exception)
    ant_login_error = pyqtSignal(list)