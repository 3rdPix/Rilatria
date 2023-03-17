from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

def hpad_this(*args) -> QVBoxLayout:
        padded_boxes: list = list()
        layout = QVBoxLayout()
        for widget in args:
            local_pad = QHBoxLayout()
            local_pad.addStretch()
            if type(widget) == type(args):
                for each in widget: local_pad.addWidget(each)
            elif type(widget) == type(QVBoxLayout) or\
                type(widget) == type(QHBoxLayout):
                local_pad.addLayout(widget)
            else: local_pad.addWidget(widget)
            local_pad.addStretch()
            padded_boxes.append(local_pad)
        for box in padded_boxes:
            layout.addStretch()
            layout.addLayout(box)
        layout.addStretch()
        return layout