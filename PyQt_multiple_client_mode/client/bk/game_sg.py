from PyQt5.QtCore import QObject, pyqtSignal


class Signals(QObject):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    ant_show_login = pyqtSignal()
    ant_wire_error = pyqtSignal(Exception)
    ant_login_error = pyqtSignal(list)
    ant_me_name = pyqtSignal(str)
    ant_go_waiting = pyqtSignal(str)
    ant_opponent_name = pyqtSignal(str)
    ant_show_game = pyqtSignal()

    ant_my_turn = pyqtSignal(bool)
    ant_update_stat = pyqtSignal(dict)