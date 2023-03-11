import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel

class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('9x9 Board')
        self.setGeometry(100, 100, 500, 500)
        self.setMinimumSize(300, 300)  # set minimum window size

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        self.setLayout(grid)

        self.squares = []
        for i in range(9):
            row = []
            for j in range(9):
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet('QLabel { border: 1px solid black;}\
                                    QWidget:hover {background-color: #b3ffff;}')
                if (i + j) % 2 == 0:
                    label.setStyleSheet('QLabel {background-color: gray;\
                                        border: 1px solid black;} \
                                        QWidget:hover {\
                                        background-color: #b3ffff;}')
                grid.addWidget(label, i, j)
                row.append(label)
            self.squares.append(row)
        grid.setSpacing(0)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.show()

    def resizeEvent(self, event):
        # ensure the labels remain as squares without deforming
        size = min(self.width(), self.height())
        for row in self.squares:
            for label in row:
                label.setFixedSize(int(size/9), int(size/9))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    sys.exit(app.exec_())
