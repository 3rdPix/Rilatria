from PyQt5.QtWidgets import QFrame, QGridLayout, QSizePolicy, QWidget, QLabel
from FrontEnd.styles import cell_style


class Board(QFrame):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.draw_squares()
        self.setLayout(self.layout)

    def draw_squares(self):
        for row, rank in enumerate('987654321'):
            for col, file in enumerate('abcdefghi'):
                square = QLabel()
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                square.setStyleSheet(cell_style)
                square.setFrameStyle(QFrame.Box | QFrame.Sunken)
                # if row % 2 == col % 2:
                #     square.setStyleSheet('background-color: #cfdbdb')
                # else:
                #     square.setStyleSheet('background-color: #51b0cc')
                self.layout.addWidget(square, row, col)



if __name__ == "__main__":
    import sys 
    from PyQt5.QtWidgets import QApplication

    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication(sys.argv)
    board: Board = Board()
    board.show()

    sys.exit(app.exec())