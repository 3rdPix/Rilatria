from PyQt5.QtWidgets import QFrame, QGridLayout, QSizePolicy, QWidget, QLabel
from PyQt5.QtCore import Qt
from ft.styles import cell_style

## Format 1 blank
# class Board(QFrame):

#     def __init__(self, **kwargs) -> None:
#         super().__init__(**kwargs)

#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.setContentsMargins(0, 0, 0, 0)

#         self.layout = QGridLayout()
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         self.layout.setSpacing(0)
#         self.draw_squares()
#         self.setLayout(self.layout)

#     def draw_squares(self):
#         for row, rank in enumerate('987654321'):
#             for col, file in enumerate('abcdefghi'):
#                 square = QLabel()
#                 square.setObjectName(file + rank)
#                 square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#                 square.setStyleSheet(cell_style)
#                 square.setFrameStyle(QFrame.Box | QFrame.Sunken)
#                 # if row % 2 == col % 2:
#                 #     square.setStyleSheet('background-color: #cfdbdb')
#                 # else:
#                 #     square.setStyleSheet('background-color: #51b0cc')
#                 self.layout.addWidget(square, row, col)


class Board(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(grid)

        self.cells: list[list[QLabel]] = []

        for i in range(9):
            row = []
            for j in range(9):
                cell = QLabel()
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet('QLabel { border: 1px solid black;}\
                                    QWidget:hover {background-color: #b3ffff;}')
                if (i + j) % 2 == 0:
                    cell.setStyleSheet('QLabel {background-color: gray;\
                                        border: 1px solid black;} \
                                        QWidget:hover {\
                                        background-color: #b3ffff;}')
                grid.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)
        
    def resizeEvent(self, event):
        # ensure the labels remain as squares without deforming
        size = min(self.width(), self.height())
        for row in self.cells:
            for label in row:
                label.setFixedSize(int(size/9), int(size/9))