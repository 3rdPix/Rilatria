from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class Board(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(0)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.cells: list[list[QLabel]] = []

        for i in range(9):
            row = []
            for j in range(9):
                cell = QLabel()
                cell.setObjectName('Cell')
                cell.setAlignment(Qt.AlignCenter)
                # if (i + j) % 2 == 0:
                grid.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)
            
        self.setLayout(grid)
        
    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        for row in self.cells:
            for label in row:
                label.setFixedSize(int(size/9), int(size/9))
        return super().resizeEvent(event)

