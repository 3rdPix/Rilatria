from app import Rilatria
import sys
import socket
import json

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    port: int = 1714
    host: str = socket.gethostbyname(socket.gethostname())

    app = Rilatria(sys.argv, host, port)
    sys.exit(app.exec())