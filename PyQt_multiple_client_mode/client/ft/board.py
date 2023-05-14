from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap


class Cell(QLabel):

    def __init__(self, sg_clicked: pyqtSignal, coords: tuple, **kwargs) -> None:
        super().__init__(**kwargs)
        self.clicked: pyqtSignal = sg_clicked
        self.clicking: bool = False
        self.coords: tuple = coords

    def mousePressEvent(self, ev) -> None:
        self.clicking = True
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev) -> None:
        if self.clicking and self.underMouse():
            self.clicking = False
            self.clicked.emit(self.coords)
        return super().mouseReleaseEvent(ev)


class Board(QWidget):
    
    def __init__(self, im_barbarian: str, im_horserider: str, im_spearman: str,
                 im_rattletrap: str, im_joker: str, im_hero: str,
                 sg_cell_clicked: pyqtSignal) -> None:
        super().__init__()
        self.icons: dict[str, QPixmap] = {
            'Barbarian': QPixmap(im_barbarian),
            'Horserider': QPixmap(im_horserider),
            'Spearman': QPixmap(im_spearman),
            'RattleTrap': QPixmap(im_rattletrap),
            'Joker': QPixmap(im_joker),
            'Hero': QPixmap(im_hero)
        }
        self.initUI(sg_cell_clicked)

    def initUI(self, sg_cell_clicked: pyqtSignal):
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(0)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.cells: list[list[QLabel]] = []

        for i in range(9):
            row = []
            for j in range(9):
                cell = Cell(sg_cell_clicked, (i, j))
                cell.setScaledContents(True)
                cell.setObjectName('Cell')
                cell.setAlignment(Qt.AlignCenter)
                # if (i + j) % 2 == 0:
                grid.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)
            
        self.setLayout(grid)
        
    def display(self, board: list) -> None:
        for my_row, real_row in zip(self.cells, board):
            for my_cell, real_piece in zip(my_row, real_row):
                if real_piece == 'X': continue
                my_cell.setPixmap(self.icons[real_piece])

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        for row in self.cells:
            for label in row:
                label.setFixedSize(int(size/9), int(size/9))
        return super().resizeEvent(event)

