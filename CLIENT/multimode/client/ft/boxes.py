from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class StatSet(QVBoxLayout):

    def __init__(self, pt_stat_icon: str, pt_text_frame: str, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.addStretch()
        icon = QLabel()
        icon.setPixmap(QPixmap(pt_stat_icon))
        icon.setScaledContents(True)
        icon.setFixedSize(60, 60)
        top = QHBoxLayout()
        top.addStretch()
        top.addWidget(icon)
        top.addStretch()
        self.addLayout(top)

        txt_frame = QLabel()
        txt_frame.setPixmap(QPixmap(pt_text_frame))
        self.value = QLabel('NA')
        self.value.setObjectName('StatLabel')
        frame_lay = QHBoxLayout()
        frame_lay.addStretch()
        frame_lay.addWidget(self.value)
        frame_lay.addStretch()
        txt_frame.setLayout(frame_lay)
        bot = QHBoxLayout()
        bot.addStretch()
        bot.addWidget(txt_frame)
        bot.addStretch()
        self.addLayout(bot)
        self.addStretch()

    def set_value(self, value: int) -> None:
        self.value.setText(str(value))


class ItemSet(QLabel):

    def __init__(self, image_path: str, name: str, background_path: str,
                 hover_path: str, click_back_path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.non_hover_back = QPixmap(background_path)
        self.hover_back = QPixmap(hover_path)
        self.click_back = QPixmap(click_back_path)
        self.setPixmap(self.non_hover_back)
        self.setScaledContents(True)
        self.set_content(image_path, name)
        self.setFixedSize(93, 121)

    def set_content(self, image_path: str, name: str) -> None:
        content_lay = QVBoxLayout()
        content_lay.addStretch()

        mob_label = QLabel()
        mob_image = QPixmap(image_path)
        mob_label.setPixmap(mob_image)
        mob_label.setScaledContents(True)
        top = QHBoxLayout()
        top.addStretch()
        top.addWidget(mob_label)
        top.addStretch()
        content_lay.addLayout(top)

        self.name_label = QLabel(text=name)
        self.name_label.setWordWrap(True)
        self.name_label.setObjectName('ItemLabel')
        bot = QHBoxLayout()
        bot.addStretch()
        bot.addWidget(self.name_label)
        bot.addStretch()
        content_lay.addLayout(bot)
        content_lay.addStretch()
        self.setLayout(content_lay)

    def redo_text(self, name: str) -> None:
        self.name_label.setText(name)

    def enterEvent(self, event) -> None:
        self.setPixmap(self.hover_back)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setPixmap(self.non_hover_back)
        return super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton: self.setPixmap(self.click_back)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.setPixmap(self.hover_back)
        return super().mouseReleaseEvent(event)
    
class TurnSet(QLabel):

    clicked = pyqtSignal()

    def __init__(self, name: str, background_path: str,
                 hover_path: str, click_back_path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.non_hover_back = QPixmap(background_path)
        self.hover_back = QPixmap(hover_path)
        self.click_back = QPixmap(click_back_path)
        self.setPixmap(self.non_hover_back)
        self.setScaledContents(True)
        self.set_content(name)
        self.setFixedSize(86, 40)

    def set_content(self, name: str) -> None:
        content_lay = QVBoxLayout()
        content_lay.addStretch()

        self.name_label = QLabel(text=name)
        self.name_label.setWordWrap(True)
        self.name_label.setObjectName('StatLabel')
        bot = QHBoxLayout()
        bot.addStretch()
        bot.addWidget(self.name_label)
        bot.addStretch()
        content_lay.addLayout(bot)
        content_lay.addStretch()
        self.setLayout(content_lay)

    def redo_text(self, name: str) -> None:
        self.name_label.setText(name)

    def enterEvent(self, event) -> None:
        self.setPixmap(self.hover_back)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setPixmap(self.non_hover_back)
        return super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton: self.setPixmap(self.click_back)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.setPixmap(self.hover_back)
        if self.underMouse(): self.clicked.emit()
        return super().mouseReleaseEvent(event)