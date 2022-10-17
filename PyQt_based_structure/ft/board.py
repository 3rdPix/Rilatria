from PyQt5.QtWidgets import QFrame, QGridLayout, QSizePolicy, QWidget


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
                square = QWidget()
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                if row % 2 == col % 2:
                    square.setStyleSheet('background-color: #cfdbdb')
                else:
                    square.setStyleSheet('background-color: #51b0cc')
                self.layout.addWidget(square, row, col)